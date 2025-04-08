interface AuthorInfo {
  name: string;
  ORCID?: string | null;
}

export interface ArticleData {
  publication: {
    title: string;
    authors: string[];
    doi: string;
    keywords: string[];
    abstract: string;
    journal: string;
    year: number;
    volume: string | null;
    number: string | null;
    pages: string;
  };
  authors_info: AuthorInfo[]; // Заменяем any[] на AuthorInfo[]
  journal_issue: JournalIssue; // Также типизируем journal_issue
  journal_info: JournalInfo; // И journal_info
}

interface JournalIssue {
  journal: string;
  year: number;
  WoS: boolean;
  Quartile_WoS: number;
  Scopus: boolean;
  Quartile_Scopus: number;
  WhiteList: boolean;
  Quartile_WL: number;
  RINC_core: boolean;
}

interface JournalInfo {
  title: string;
  ISSN?: string;
  eISSN?: string;
  publisher?: string;
}
