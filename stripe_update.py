import stripe
import os
import datetime

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def update_subscriptions():
    print(f"Starting billing sync for {datetime.date.today()}...")
    subscriptions = stripe.Subscription.list(status='active', limit=100)
    count = 0
    for sub in subscriptions.auto_paging_iter():
        try:
            stripe.Subscription.modify(
                sub.id,
                billing_cycle_anchor='now',
                proration_behavior='always_invoice'
            )
            print(f"Successfully updated: {sub.id}")
            count += 1
        except Exception as e:
            print(f"Failed to update {sub.id}: {e}")
    print(f"Finished. Updated {count} subscriptions.")

if __name__ == "__main__":
    update_subscriptions()
