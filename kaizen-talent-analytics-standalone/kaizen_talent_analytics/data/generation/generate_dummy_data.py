import csv
import random
from datetime import datetime, timedelta

def generate_dummy_ats_events(filename: str, num_rows: int = 10) -> None:
    """
    Generate dummy ATS event data and save to CSV.

    Args:
        filename (str): Output CSV file path.
        num_rows (int): Number of rows to generate.

    Returns:
        None
    """
    stages = ['Sourced', 'Screened', 'Interview', 'Hired', 'Rejected']
    sources = ['LinkedIn', 'Referral', 'Job Board', 'Career Fair']
    outcomes = ['Passed', 'Failed', 'Pending']

    start_date = datetime.now() - timedelta(days=90)

    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['candidate_id', 'source', 'stage', 'outcome', 'timestamp'])

        for i in range(1, num_rows + 1):
            candidate_id = f"C{i:05d}"
            source = random.choice(sources)
            stage = random.choice(stages)
            outcome = random.choice(outcomes)
            timestamp = (start_date + timedelta(days=random.randint(0, 90),
                                                hours=random.randint(0, 23),
                                                minutes=random.randint(0, 59))).isoformat()
            writer.writerow([candidate_id, source, stage, outcome, timestamp])

if __name__ == "__main__":
    generate_dummy_ats_events("data/dummy_ats_events.csv", num_rows=20)
