import { useEffect, useState, useCallback } from "react";
import axios from "axios";
import { Publication } from "../../../publication";

export const useArticleStore = () => {
  const [articles, setArticles] = useState<Publication[]>([]);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);

  const fetchArticles = useCallback(
    async (query = search, pageNum = page) => {
      try {
        const res = await axios.get("http://127.0.0.1:8000/publications", {
          params: { page: pageNum, query },
        });
        setArticles(res.data);
      } catch {
        setArticles([]);
      }
    },
    [search, page]
  );

  const refreshArticles = async () => {
    await fetchArticles("", 1);
    setPage(1);
    setSearch("");
  };

  useEffect(() => {
    fetchArticles();
  }, [fetchArticles]);

  return { articles, search, setSearch, page, setPage, refreshArticles };
};
