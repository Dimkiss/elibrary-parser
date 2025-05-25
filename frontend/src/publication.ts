export interface Publication {
  title: string;
  doi: string;
  authors: string[];
  journal: string | null;
  year: number;
}
