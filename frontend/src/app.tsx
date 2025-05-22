import { useState, useEffect } from "react";
import axios from "axios";

const App = () => {
  const [doi, setDoi] = useState("");
  const [data, setData] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const [articles, setArticles] = useState<any[]>([]);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/publications", {
        params: { page, query: search },
      })
      .then((res) => setArticles(res.data))
      .catch(() => setArticles([]));
  }, [search, page]);

  const handleSearch = async () => {
    setError(null);
    setData(null);
    setLoading(true);
    try {
      const response = await axios.get("http://127.0.0.1:8000/parse-lite", {
        params: { doi },
      });
      setData(response.data);
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Ошибка запроса");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1 style={{ fontSize: "1.5rem", marginBottom: "1rem" }}>Поиск по DOI</h1>
      <div style={{ marginBottom: "1rem" }}>
        <input
          type="text"
          value={doi}
          onChange={(e) => setDoi(e.target.value)}
          placeholder="Введите DOI"
          style={{ padding: "0.5rem", width: "300px", marginRight: "1rem" }}
        />
        <button onClick={handleSearch} style={{ padding: "0.5rem 1rem" }}>
          Поиск
        </button>
      </div>

      {loading && <p>Загрузка...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {data && (
        <div
          style={{
            background: "#f9f9f9",
            padding: "1rem",
            borderRadius: "4px",
            maxWidth: "800px",
            marginBottom: "2rem",
          }}
        >
          <h2>📄 Публикация</h2>
          <p>
            <strong>Название:</strong> {data.publication.title}
          </p>
          <p>
            <strong>DOI:</strong> {data.publication.doi}
          </p>
          <p>
            <strong>Авторы:</strong> {data.publication.authors.join(", ")}
          </p>
          <p>
            <strong>Журнал:</strong> {data.publication.journal}
          </p>
          <p>
            <strong>Год:</strong> {data.publication.year}
          </p>
        </div>
      )}

      <h2>📚 Публикации</h2>
      <input
        placeholder="Поиск по DOI, автору, названию..."
        value={search}
        onChange={(e) => {
          setSearch(e.target.value);
          setPage(1);
        }}
        style={{ padding: "0.5rem", width: "300px", marginBottom: "1rem" }}
      />
      <ul>
        {articles.map((art, i) => (
          <li key={i} style={{ marginBottom: "1rem" }}>
            <strong>{art.title}</strong> ({art.year})<br />
            <small>
              DOI: {art.doi}
              <br />
              Авторы: {art.authors.join(", ")}
              <br />
              Журнал: {art.journal}
            </small>
          </li>
        ))}
      </ul>
      <div>
        <button onClick={() => setPage((p) => Math.max(p - 1, 1))}>
          ← Назад
        </button>
        <span style={{ margin: "0 1rem" }}>Стр. {page}</span>
        <button onClick={() => setPage((p) => p + 1)}>Вперёд →</button>
      </div>
    </div>
  );
};

export default App;
