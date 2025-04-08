export function Card({ children }: { children: React.ReactNode }) {
  return (
    <div className="border rounded p-4 shadow-sm bg-white">{children}</div>
  );
}
