import DoiInput from "../features/DoiInput/ui/DoiInput";
import ArticleList from "../features/ArticleList/ui/ArticleList";
import styles from "../styles.module.css";

const HomePage = () => (
  <div className={styles.container}>
    <ArticleList />
    <DoiInput />
  </div>
);

export default HomePage;
