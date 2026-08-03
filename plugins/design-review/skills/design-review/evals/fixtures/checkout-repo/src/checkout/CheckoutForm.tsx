import { useState } from "react";

export function CheckoutForm({ onSubmit }: { onSubmit: (d: FormData) => void }) {
  const [step, setStep] = useState(0);
  const [errors, setErrors] = useState<Record<string, string>>({});

  return (
    <div className="checkout">
      <div className="steps">
        <span className={step === 0 ? "on" : ""}>Shipping</span>
        <span className={step === 1 ? "on" : ""}>Payment</span>
        <span className={step === 2 ? "on" : ""}>Review</span>
      </div>

      {step === 0 && (
        <form onSubmit={(e) => { e.preventDefault(); setStep(1); }}>
          <input placeholder="Full name" name="name" />
          <input placeholder="Address line 1" name="addr1" />
          <input placeholder="Postcode" name="postcode" type="number" />
          <input placeholder="Email" name="email" />
          <input placeholder="Confirm email" name="email2" />
          <div onClick={() => setStep(1)} className="btn primary" role="button">
            Continue
          </div>
        </form>
      )}

      {step === 1 && (
        <form onSubmit={(e) => { e.preventDefault(); setStep(2); }}>
          <input placeholder="Card number" name="card" type="number" />
          <input placeholder="MM/YY" name="exp" />
          <input placeholder="CVC" name="cvc" />
          {errors.card && <span style={{ color: "#e11" }}>{errors.card}</span>}
          <button className="btn primary">Continue</button>
        </form>
      )}

      {step === 2 && (
        <div>
          <p>Almost there! Only 2 left in stock — order now!</p>
          <button className="btn primary" onClick={() => onSubmit(new FormData())}>
            Submit
          </button>
          <a href="#" onClick={() => setStep(0)}>go back</a>
        </div>
      )}
    </div>
  );
}
