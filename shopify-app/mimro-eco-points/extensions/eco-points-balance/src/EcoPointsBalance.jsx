import '@shopify/ui-extensions/preact';
import {render} from 'preact';
import {useEffect, useState} from 'preact/hooks';

const API_VERSION = '2026-07';
const SHOP_URL = 'https://www.mimro.com/collections/all';
const EARN_URL = 'https://www.mimro.com/pages/eco-quest';
const POINTS_PER_CODE = 500;

const QUERY = `query {
  customer {
    points: metafield(namespace: "eco_quest", key: "points") { value }
    lifetime: metafield(namespace: "eco_quest", key: "lifetime_points") { value }
  }
}`;

export default async () => {
  render(<EcoPointsBalance />, document.body);
};

function EcoPointsBalance() {
  const [balance, setBalance] = useState(null);

  useEffect(() => {
    fetch(`shopify://customer-account/api/${API_VERSION}/graphql.json`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({query: QUERY}),
    })
      .then((response) => response.json())
      .then(({data}) => {
        const customer = data?.customer;
        setBalance({
          points: Number(customer?.points?.value ?? 0),
          lifetime: Number(customer?.lifetime?.value ?? 0),
        });
      })
      .catch(() => setBalance({points: 0, lifetime: 0}));
  }, []);

  if (!balance) {
    return <s-text color="subdued">Loading your Eco Points…</s-text>;
  }

  // 100 points = $1
  const dollars = shopify.i18n.formatCurrency(balance.points / 100, {
    currency: 'CAD',
  });
  const toNext = POINTS_PER_CODE - (balance.points % POINTS_PER_CODE);

  return (
    <s-section heading="Mimro Eco Points">
      <s-stack direction="block" gap="small-200">
        <s-text type="strong">
          Eco Points Balance: {balance.points} pts = {dollars}
        </s-text>
        <s-text color="subdued">
          {toNext} more points to your next $5 off code · Lifetime{' '}
          {balance.lifetime} pts
        </s-text>
        <s-stack direction="inline" gap="base">
          <s-button href={SHOP_URL}>Continue shopping</s-button>
          <s-button variant="secondary" href={EARN_URL}>
            Earn more points
          </s-button>
        </s-stack>
      </s-stack>
    </s-section>
  );
}
