"""Optional read-only export of HubSpot contacts and deals to CSV."""
import os
from pathlib import Path
import requests
import pandas as pd

BASE_URL = "https://api.hubapi.com"
OUT = Path(__file__).resolve().parent / "powerbi" / "exports"


def fetch_objects(object_type, properties):
    token = os.getenv("HUBSPOT_ACCESS_TOKEN")
    if not token:
        raise SystemExit("Set HUBSPOT_ACCESS_TOKEN to your authorized HubSpot private-app token.")
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{BASE_URL}/crm/v3/objects/{object_type}"
    params = {"limit": 100, "properties": ",".join(properties)}
    rows = []
    while url:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        if response.status_code == 401:
            raise SystemExit("HubSpot rejected the token. Check the token and app scopes.")
        response.raise_for_status()
        payload = response.json()
        rows.extend({"id": item.get("id"), **item.get("properties", {})}
                    for item in payload.get("results", []))
        after = payload.get("paging", {}).get("next", {}).get("after")
        if after is None:
            break
        params["after"] = after
    return rows


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    contacts = fetch_objects("contacts", [
        "email", "createdate", "lifecyclestage", "hs_lead_status", "hubspot_owner_id"])
    deals = fetch_objects("deals", [
        "dealname", "amount", "dealstage", "pipeline", "closedate", "createdate",
        "hubspot_owner_id"])
    pd.DataFrame(contacts).to_csv(OUT / "hubspot_contacts.csv", index=False)
    pd.DataFrame(deals).to_csv(OUT / "hubspot_deals.csv", index=False)
    print(f"Exported {len(contacts)} contacts and {len(deals)} deals to {OUT}")


if __name__ == "__main__":
    main()
