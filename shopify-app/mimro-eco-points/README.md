# Mimro Eco Points – customer account extension

Shows the signed-in customer's balance on the Orders and Profile pages of
Shopify customer accounts:

> **Eco Points Balance: 449 pts = $4.49**
> 51 more points to your next $5 off code · Lifetime 449 pts
> [Continue shopping] [Earn more points]

The balance comes from the customer metafields `eco_quest.points` and
`eco_quest.lifetime_points` (100 points = $1), which the weekly
"Eco Points weekly credit" routine keeps up to date. Those metafield
definitions already have Customer account access set to **Read**.

## Deploy (one time, about 10 minutes)

Needs Node 20+ and the Shopify account that owns mimro.com.

```bash
cd shopify-app/mimro-eco-points
npm install
npx shopify app config link   # create a new app called "Mimro Eco Points"
npx shopify app deploy        # publishes the extension
npx shopify app dev           # optional: preview before installing
```

Then in Shopify admin:

1. Install the app on the store when prompted.
2. **Settings → Checkout and accounts → Customize** (customer accounts),
   open the **Orders** page, click **Add app block** and choose
   **Mimro Eco Points balance**. Drag it to the top. Repeat on **Profile** if wanted.
3. **Save**.

If the block shows 0 for everyone, check that the app has
`customer_read_customers` and that protected customer data access
(level 1, name not needed) is enabled for the app in the Dev Dashboard.
