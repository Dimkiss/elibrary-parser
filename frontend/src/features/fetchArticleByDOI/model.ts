import { api } from "../../shared/api/instance";
import { ArticleData } from "./types";

export async function fetchArticleByDOI(doi: string): Promise<ArticleData> {
  const response = await api.get("/parse", { params: { doi } });
  return response.data;
}
