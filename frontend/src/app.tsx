import { useState } from "react";
import axios from "axios";

const App = () => {
  const [doi, setDoi] = useState("");
  const [data, setData] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setError(null);
    setData(null);
    setLoading(true);
    try {
      const response = await axios.get("http://127.0.0.1:8000/parse", {
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
        <div style={{ background: "#f9f9f9", padding: "1rem", borderRadius: "4px", maxWidth: "800px" }}>
          <h2>📄 Публикация</h2>
          <p><strong>Название:</strong> {data.publication.title}</p>
          <p><strong>DOI:</strong> {data.publication.doi}</p>
          <p><strong>Авторы:</strong> {data.publication.authors.join(", ")}</p>
          <p><strong>Журнал:</strong> {data.publication.journal}</p>
          <p><strong>Год:</strong> {data.publication.year}</p>
          <p><strong>Том:</strong> {data.publication.volume || "-"}</p>
          <p><strong>Номер:</strong> {data.publication.number || "-"}</p>
          <p><strong>Страницы:</strong> {data.publication.pages}</p>
          <p><strong>Ключевые слова:</strong> {data.publication.keywords.join(", ")}</p>
          <p><strong>Аннотация:</strong> {data.publication.abstract}</p>

          <h2 style={{ marginTop: "1rem" }}>👤 Авторы (подробно)</h2>
          {data.authors_info.map((a: any, idx: number) => (
            <div key={idx} style={{ marginBottom: "0.5rem" }}>
              <p><strong>ФИО:</strong> {a.lastname} {a.name} {a.patronymic || ""}</p>
              <p><strong>Аффилиация:</strong> {a.affiliation.join(", ")}</p>
              <p><strong>ORCID:</strong> {a.ORCID || "-"}</p>
            </div>
          ))}

          <h2 style={{ marginTop: "1rem" }}>📘 Выпуск журнала</h2>
          <p><strong>Журнал:</strong> {data.journal_issue.journal}</p>
          <p><strong>Год:</strong> {data.journal_issue.year}</p>
          <p><strong>WoS:</strong> {data.journal_issue.WoS ? "Да" : "Нет"}</p>
          <p><strong>Quartile WoS:</strong> {data.journal_issue.Quartile_WoS}</p>
          <p><strong>Scopus:</strong> {data.journal_issue.Scopus ? "Да" : "Нет"}</p>
          <p><strong>Quartile Scopus:</strong> {data.journal_issue.Quartile_Scopus}</p>
          <p><strong>WhiteList:</strong> {data.journal_issue.WhiteList ? "Да" : "Нет"}</p>
          <p><strong>Quartile WL:</strong> {data.journal_issue.Quartile_WL}</p>
          <p><strong>RINC core:</strong> {data.journal_issue.RINC_core ? "Да" : "Нет"}</p>

          <h2 style={{ marginTop: "1rem" }}>🏷 Информация о журнале</h2>
          <p><strong>Название:</strong> {data.journal_info.title}</p>
          <p><strong>ISSN:</strong> {data.journal_info.ISSN || "-"}</p>
          <p><strong>eISSN:</strong> {data.journal_info.eISSN || "-"}</p>
          <p><strong>Издатель:</strong> {data.journal_info.publisher || "-"}</p>
        </div>
      )}
    </div>
  );
};

export default App;
