import { DOISearch } from "../../widgets/DOISearch/ui";
import { ArticleResult } from "../../widgets/ArticleResult/ui";
import { useState } from "react";
import { ArticleData } from "../../features/fetchArticleByDOI/types";

export function HomePage() {
  const [data, setData] = useState<ArticleData | null>(null);

  return (
    <main className="max-w-3xl mx-auto p-6 space-y-6">
      <DOISearch onResult={setData} />
      {data && <ArticleResult data={data} />}
    </main>
  );
}
