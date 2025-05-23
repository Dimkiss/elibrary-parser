import { useDoiInput } from "../model/useDoiInput";
import styles from "../../../styles.module.css";

const DoiInput = () => {
  const { doi, setDoi, loading, error, success, handleElibraryAdd } =
    useDoiInput();

  return (
    <>
      <h1 className={styles.heading}>Не нашли нужную статью?</h1>
      <div className={styles.inputRow}>
        <input
          type="text"
          value={doi}
          onChange={(e) => setDoi(e.target.value)}
          placeholder="Введите DOI"
          className={styles.input}
        />
        <button onClick={handleElibraryAdd} className={styles.button}>
          Найти в eLibrary
        </button>
      </div>
      {loading && <p>Загрузка...</p>}
      {error && <p className={styles.error}>{error}</p>}
      {success && <p className={styles.success}>{success}</p>}
    </>
  );
};

export default DoiInput;
