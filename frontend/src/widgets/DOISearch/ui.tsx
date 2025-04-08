import { useState } from "react";
import { Input } from "../../shared/ui/Input";
import { Button } from "../../shared/ui/Button";
import { fetchArticleByDOI } from "../../features/fetchArticleByDOI/model";
import { ArticleData } from "../../features/fetchArticleByDOI/types";

interface Props {
  onResult: (data: ArticleData) => void;
}

export function DOISearch({ onResult }: Props) {
  const [doi, setDOI] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    const data = await fetchArticleByDOI(doi);
    onResult(data);
    setLoading(false);
  };

  return (
    <div className="flex gap-4">
      <Input
        value={doi}
        onChange={(e) => setDOI(e.target.value)}
        placeholder="Enter DOI..."
      />
      <Button onClick={handleSearch} disabled={loading}>
        {loading ? "Loading..." : "Parse"}
      </Button>
    </div>
  );
}
