const PLANS = [
  { name: "Starter", price: 0, blurb: "For trying things out" },
  { name: "Team", price: 24, blurb: "For small teams", popular: true },
  { name: "Scale", price: 96, blurb: "For growing companies", popular: false },
];

export function PlanCards() {
  return (
    <div className="plans">
      {PLANS.map((p) => (
        <div key={p.name} className={`plan ${p.popular ? "popular" : ""}`}>
          {p.popular && <span className="badge">Most popular</span>}
          <h3>{p.name}</h3>
          <div className="price">
            <span className="amount">${p.price}</span>
            <span className="per">/mo</span>
          </div>
          <p>{p.blurb}</p>
          <div className="btn" role="button" onClick={() => {}}>
            Get started
          </div>
        </div>
      ))}
    </div>
  );
}
