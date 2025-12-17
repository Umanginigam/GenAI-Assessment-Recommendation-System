import pandas as pd
import re

INPUT_PATH = "shl_individual_test_solutions.csv"
OUTPUT_PATH = "data/shl_catalog_clean.csv"

def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def normalize_test_type(raw):
    raw = str(raw).upper()

    # Knowledge & Skills
    if "K" in raw:
        return "K"

    # Simulation / Work Sample
    if "S" in raw:
        return "S"

    # Personality / Behavioral family
    if any(x in raw for x in ["P", "A", "B", "C", "D", "E"]):
        return "P"

    return "Unknown"


def main():
    df = pd.read_csv(INPUT_PATH, header=None)

    # Explicit column mapping (VERY IMPORTANT)
    df_clean = pd.DataFrame({
        "assessment_name": df[0].apply(clean_text),
        "url": df[1].apply(clean_text),
        "description": df[3].apply(clean_text),
        "raw_test_type": df[8].apply(clean_text)
    })

    df_clean["test_type"] = df_clean["raw_test_type"].apply(normalize_test_type)

    # Build embedding-ready text
    df_clean["search_text"] = (
    "Assessment Name: " + df_clean["assessment_name"] + ". " +
    "Description: " + df_clean["description"] + ". " +
    "Assessment Type: " + df_clean["test_type"] + ". " +
    "This assessment is suitable for evaluating relevant job skills."
)


    df_clean = df_clean.dropna(subset=["assessment_name", "url"])
    df_clean = df_clean.drop_duplicates(subset=["url"])

    df_clean.to_csv(OUTPUT_PATH, index=False)

    print("✅ Clean dataset saved:", OUTPUT_PATH)
    print("✅ Total assessments:", len(df_clean))
    assert len(df_clean) >= 377, "❌ Less than required assessments"
    assert df_clean["test_type"].isin(["K", "P", "S"]).all(), "❌ Unknown test types found"
    assert df_clean["url"].str.startswith("https").all(), "❌ Invalid URLs detected"


if __name__ == "__main__":
    main()
