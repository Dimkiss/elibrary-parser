import { useArticleStore } from "../model/useArticleStore";
import styles from "../../../styles.module.css";

const ArticleList = () => {
  const { articles, page, setPage, search, setSearch } = useArticleStore();

  return (
    <>
      <h1>Публикации</h1>
      <input
        placeholder="Поиск по DOI, автору, названию..."
        value={search}
        onChange={(e) => {
          setSearch(e.target.value);
          setPage(1);
        }}
        className={styles.input}
      />
      <ul>
        {articles.map((art, i) => (
          <li key={i} className={styles.articleItem}>
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
        <button
          onClick={() => setPage((p) => Math.max(p - 1, 1))}
          className={styles.button}
        >
          ← Назад
        </button>

        <span className={styles.pagination}>Стр. {page}</span>

        <button
          onClick={() => setPage((p) => p + 1)}
          className={styles.button}
        >
          Вперёд →
        </button>
      </div>
    </>
  );
};

export default ArticleList;
