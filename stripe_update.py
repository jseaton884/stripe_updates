import stripe
import os
import sys

# Get and clean the key
raw_key = os.getenv("STRIPE_SECRET_KEY", "")
key = raw_key.strip().replace('"', '').replace("'", "")

if not key:
    print("ERROR: Secret Key is empty. Check GitHub Secrets.")
    sys.exit(1)

# Safety check: Print the length and prefix only
print(f"Debug: Key starts with {key[:7]} and is {len(key)} characters long.")

stripe.api_key = key

def update_subscriptions():
    try:
        # Just a simple connectivity test
        acc = stripe.Account.retrieve()
        print(f"Connected to Stripe Account: {acc.id}")
        
        subscriptions = stripe.Subscription.list(status="active", limit=10)
        print(f"Found {len(subscriptions)} subscriptions to review.")
        
        for sub in subscriptions:
            # (Logic for Feb 1st filtering goes here once connection works)
            print(f"Would process: {sub.id}")
            
    except Exception as e:
        print(f"CONNECTION ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    update_subscriptions()