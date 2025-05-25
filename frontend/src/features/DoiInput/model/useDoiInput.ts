import { useState } from "react";
import axios from "axios";

export const useDoiInput = () => {
  const [doi, setDoi] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const handleElibraryAdd = async () => {
    setError(null);
    setSuccess(null);
    setLoading(true);
    try {
      await axios.post("http://127.0.0.1:8000/parse-by-doi-online", null, {
        params: { doi },
      });

      localStorage.setItem("articleAdded", "1");

      window.location.reload();
    } catch (err: unknown) {
      if (axios.isAxiosError(err)) {
        setError(err.response?.data?.detail || "Ошибка при запросе к eLibrary");
      } else {
        setError("Неизвестная ошибка");
      }
    } finally {
      setLoading(false);
    }
  };

  return { doi, setDoi, loading, error, success, handleElibraryAdd };
};
