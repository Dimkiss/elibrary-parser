import { ArticleData } from "../../features/fetchArticleByDOI/types";
import { Card } from "../../shared/ui/Card";

interface Props {
  data: ArticleData;
}

export function ArticleResult({ data }: Props) {
  return (
    <Card>
      <h2 className="text-xl font-bold mb-2">{data.publication.title}</h2>
      <p>
        <b>DOI:</b> {data.publication.doi}
      </p>
      <p>
        <b>Authors:</b> {data.publication.authors.join(", ")}
      </p>
      <p>
        <b>Abstract:</b> {data.publication.abstract}
      </p>
      <p>
        <b>Journal:</b> {data.publication.journal} ({data.publication.year})
      </p>
    </Card>
  );
}
