import asyncio
import csv
import json
from datetime import datetime
from typing import List, Dict, Optional
import logging
from playwright.async_api import async_playwright, Page, Browser
import sys
import re

# Configuration
CONFIG = {
    'base_url': 'https://www.shl.com/products/product-catalog/',
    'timeout': 30000,
    'retry_attempts': 3,
    'retry_delay': 2000,
    'output_file': 'shl_individual_test_solutions.csv',
    'navigation_timeout': 60000,
    'min_products': 377,
    'max_pages': 32,
    'items_per_page': 12
}

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


async def delay(ms: int):
    """Delay execution for specified milliseconds"""
    await asyncio.sleep(ms / 1000)


async def with_retry(func, retries: int = CONFIG['retry_attempts']):
    """Retry wrapper for async functions"""
    for i in range(retries):
        try:
            return await func()
        except Exception as error:
            logger.warning(f"Attempt {i + 1} failed: {str(error)}")
            if i == retries - 1:
                raise error
            await delay(CONFIG['retry_delay'] * (i + 1))


def get_pagination_url(page_num: int) -> str:
    """Generate pagination URL for given page number"""
    if page_num == 1:
        return f"{CONFIG['base_url']}?type=1"
    
    start = (page_num - 1) * CONFIG['items_per_page']
    # Based on the pattern, type=1 appears multiple times after page 2
    if page_num == 2:
        return f"{CONFIG['base_url']}?start={start}&type=1"
    else:
        return f"{CONFIG['base_url']}?start={start}&type=1&type=1"


async def get_products_from_page(page: Page, page_num: int) -> List[Dict[str, str]]:
    """Scrape products from a single catalog page"""
    url = get_pagination_url(page_num)
    logger.info(f'Loading page {page_num}: {url}')
    
    async def navigate():
        await page.goto(
            url,
            wait_until='networkidle',
            timeout=CONFIG['navigation_timeout']
        )
    
    await with_retry(navigate)
    await page.wait_for_timeout(3000)
    
    # Find the "Individual Test Solutions" table
    products = []
    
    try:
        # Wait for the table to load
        await page.wait_for_selector('table tbody tr', timeout=10000)
        
        # Extract products from the Individual Test Solutions table
        products_data = await page.evaluate('''() => {
            const products = [];
            
            // Find all tables on the page
            const tables = document.querySelectorAll('table');
            
            for (const table of tables) {
                // Check if this table has "Individual Test Solutions" heading
                const headings = table.querySelectorAll('th');
                let isIndividualTestSolutions = false;
                
                for (const heading of headings) {
                    if (heading.textContent.includes('Individual Test Solutions')) {
                        isIndividualTestSolutions = true;
                        break;
                    }
                }
                
                if (isIndividualTestSolutions) {
                    // Get all rows except the header
                    const rows = table.querySelectorAll('tbody tr');
                    
                    for (const row of rows) {
                        // Skip header rows
                        if (row.querySelector('th')) continue;
                        
                        // Find the link in the first cell
                        const link = row.querySelector('td a') || row.querySelector('a');
                        
                        if (link && link.href) {
                            const name = link.textContent.trim();
                            const url = link.href;
                            
                            // Get additional table data
                            const cells = row.querySelectorAll('td');
                            const remoteTesting = cells[1] ? cells[1].textContent.trim() : '';
                            const adaptive = cells[2] ? cells[2].textContent.trim() : '';
                            const testType = cells[3] ? cells[3].textContent.trim() : '';
                            
                            if (name && url) {
                                products.push({
                                    name: name,
                                    url: url,
                                    remoteTesting: remoteTesting,
                                    adaptive: adaptive,
                                    testType: testType
                                });
                            }
                        }
                    }
                    break; // Found the right table, no need to continue
                }
            }
            
            return products;
        }''')
        
        products = products_data
        logger.info(f'Found {len(products)} products on page {page_num}')
        
    except Exception as e:
        logger.error(f'Error extracting products from page {page_num}: {str(e)}')
    
    return products


async def get_all_product_links(page: Page) -> List[Dict[str, str]]:
    """Scrape all product links from all pages with pagination"""
    all_products = []
    
    for page_num in range(1, CONFIG['max_pages'] + 1):
        logger.info(f'\n=== Processing page {page_num}/{CONFIG["max_pages"]} ===')
        
        try:
            products = await get_products_from_page(page, page_num)
            
            if not products:
                logger.warning(f'No products found on page {page_num}. May have reached the end.')
                # If we get 3 consecutive empty pages, stop
                if page_num > 3:
                    break
            
            all_products.extend(products)
            logger.info(f'Total products collected so far: {len(all_products)}')
            
            # Be respectful - add delay between page loads
            await delay(2000)
            
        except Exception as e:
            logger.error(f'Error on page {page_num}: {str(e)}')
            continue
    
    # Remove duplicates based on URL
    seen_urls = set()
    unique_products = []
    for product in all_products:
        if product['url'] not in seen_urls:
            seen_urls.add(product['url'])
            unique_products.append(product)
    
    logger.info(f'\n=== Total unique products found: {len(unique_products)} ===')
    return unique_products


async def scrape_product_details(page: Page, product: Dict[str, str]) -> Dict[str, str]:
    """Scrape individual product details"""
    logger.info(f"Scraping: {product['name']}")
    
    try:
        async def navigate():
            await page.goto(
                product['url'],
                wait_until='networkidle',
                timeout=CONFIG['navigation_timeout']
            )
        
        await with_retry(navigate)
        await page.wait_for_timeout(2000)
        
        # Extract product details with fallbacks
        details = await page.evaluate('''() => {
            const getTextContent = (selectors) => {
                for (const selector of selectors) {
                    const element = document.querySelector(selector);
                    if (element) return element.textContent.trim();
                }
                return '';
            };
            
            const getAllTextContent = (selectors) => {
                const results = [];
                for (const selector of selectors) {
                    const elements = document.querySelectorAll(selector);
                    elements.forEach(el => {
                        const text = el.textContent.trim();
                        if (text) results.push(text);
                    });
                }
                return results.join(' | ');
            };
            
            const getMetaContent = (name) => {
                const meta = document.querySelector(`meta[name="${name}"]`) || 
                           document.querySelector(`meta[property="${name}"]`);
                return meta ? meta.getAttribute('content') : '';
            };
            
            return {
                title: getTextContent([
                    'h1.product-title',
                    'h1.hero-title',
                    'h1',
                    '.page-title',
                    '.product-name'
                ]),
                description: getTextContent([
                    '.product-description',
                    '.description',
                    '.intro-text',
                    'p.lead',
                    '.summary',
                    '.hero-description'
                ]) || getMetaContent('description'),
                overview: getTextContent([
                    '.overview',
                    '.product-overview',
                    '.about-product'
                ]),
                category: getTextContent([
                    '.product-category',
                    '.category',
                    '.breadcrumb li:last-child',
                    '.product-type'
                ]),
                features: getAllTextContent([
                    '.feature-item',
                    '.features li',
                    '.benefits li',
                    '.key-features li',
                    '.feature-list li'
                ]),
                benefits: getAllTextContent([
                    '.benefit-item',
                    '.benefits-list li',
                    '.advantages li'
                ]),
                details: getAllTextContent([
                    '.detail-item',
                    '.specifications li',
                    '.product-details p',
                    '.overview p',
                    '.product-info p'
                ]),
                duration: getTextContent([
                    '.duration',
                    '.test-duration',
                    '*[class*="duration"]'
                ]),
                language: getTextContent([
                    '.language',
                    '.languages',
                    '*[class*="language"]'
                ])
            };
        }''')
        
        return {
            'name': product['name'],
            'url': product['url'],
            'title': details.get('title') or product['name'],
            'description': details.get('description', ''),
            'overview': details.get('overview', ''),
            'category': details.get('category', ''),
            'remote_testing': product.get('remoteTesting', ''),
            'adaptive_irt': product.get('adaptive', ''),
            'test_type': product.get('testType', ''),
            'features': details.get('features', ''),
            'benefits': details.get('benefits', ''),
            'details': details.get('details', ''),
            'duration': details.get('duration', ''),
            'language': details.get('language', ''),
            'scraped_at': datetime.now().isoformat(),
            'status': 'success'
        }
        
    except Exception as error:
        logger.error(f"Error scraping {product['name']}: {str(error)}")
        return {
            'name': product['name'],
            'url': product['url'],
            'title': product['name'],
            'description': 'Failed to scrape',
            'overview': '',
            'category': '',
            'remote_testing': product.get('remoteTesting', ''),
            'adaptive_irt': product.get('adaptive', ''),
            'test_type': product.get('testType', ''),
            'features': '',
            'benefits': '',
            'details': '',
            'duration': '',
            'language': '',
            'scraped_at': datetime.now().isoformat(),
            'status': 'error',
            'error': str(error)
        }


def save_to_csv(data: List[Dict[str, str]], filename: str):
    """Save scraped data to CSV file"""
    if not data:
        logger.warning('No data to save')
        return
    
    headers = [
        'name', 'url', 'title', 'description', 'overview', 'category',
        'remote_testing', 'adaptive_irt', 'test_type', 'features', 
        'benefits', 'details', 'duration', 'language', 'scraped_at', 'status'
    ]
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data)
    
    logger.info(f'Data saved to {filename}')


def save_to_json(data: List[Dict[str, str]], filename: str):
    """Save scraped data to JSON file (backup)"""
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=2, ensure_ascii=False)
    
    logger.info(f'Backup saved to {filename}')


async def scrape_shl():
    """Main scraper function"""
    async with async_playwright() as p:
        browser: Browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = await context.new_page()
        page.set_default_timeout(CONFIG['timeout'])
        
        try:
            # Get all product links from all pages
            products = await get_all_product_links(page)
            
            if not products:
                raise Exception('No products found. The website structure may have changed.')
            
            logger.info(f"\n=== Starting to scrape {len(products)} individual test solutions ===\n")
            
            # Save the product list before scraping details
            save_to_json(products, 'product_list.json')
            
            # Scrape each product with progress tracking
            results = []
            for i, product in enumerate(products):
                logger.info(f'Progress: {i + 1}/{len(products)}')
                details = await scrape_product_details(page, product)
                results.append(details)
                
                # Save intermediate results every 50 products
                if (i + 1) % 50 == 0:
                    save_to_csv(results, f'{CONFIG["output_file"]}.backup')
                    save_to_json(results, f'{CONFIG["output_file"]}.backup.json')
                    logger.info(f'Backup saved at {i + 1} products')
                
                # Be respectful - add delay between requests
                await delay(1500)
            
            # Save final results
            save_to_csv(results, CONFIG['output_file'])
            save_to_json(results, CONFIG['output_file'].replace('.csv', '.json'))
            
            logger.info(f'\n✅ Scraping completed!')
            logger.info(f'Total products scraped: {len(results)}')
            logger.info(f'Output file: {CONFIG["output_file"]}')
            
            # Validation
            successful = sum(1 for r in results if r.get('status') == 'success')
            logger.info(f'Successful scrapes: {successful}')
            logger.info(f'Failed scrapes: {len(results) - successful}')
            
            if len(results) >= CONFIG['min_products']:
                logger.info(f'✅ Success! Found {len(results)} products (minimum {CONFIG["min_products"]} required)')
            else:
                logger.warning(f'⚠️  Warning: Only found {len(results)} products (minimum {CONFIG["min_products"]} required)')
            
            return results
            
        except Exception as error:
            logger.error(f'Fatal error: {str(error)}')
            raise error
        finally:
            await browser.close()


async def main():
    """Entry point"""
    try:
        results = await scrape_shl()
        logger.info('\n🎉 Scraping job completed successfully!')
        return results
    except Exception as error:
        logger.error(f'\n❌ Scraping job failed: {str(error)}')
        sys.exit(1)


if __name__ == '__main__':
    asyncio.run(main())