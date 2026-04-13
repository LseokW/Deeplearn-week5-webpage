import { useState, useEffect } from "react";
import client from "../api/client";

export function usePurchase() {
  const [purchased, setPurchased] = useState(false);
  const [loading, setLoading] = useState(true);

  async function checkPurchase() {
    try {
      const res = await client.get("/api/payment/status");
      setPurchased(res.data.data.purchased);
    } catch {
      setPurchased(false);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    checkPurchase();
  }, []);

  return { purchased, loading, refetch: checkPurchase };
}
