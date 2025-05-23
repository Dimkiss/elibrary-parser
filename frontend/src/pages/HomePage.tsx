import DoiInput from "../features/DoiInput/ui/DoiInput";
import ArticleList from "../features/ArticleList/ui/ArticleList";

const HomePage = () => (
  <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
    <DoiInput />
    <ArticleList />
  </div>
);

export default HomePage;
