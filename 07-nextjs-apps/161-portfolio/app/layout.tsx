import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Attanti Ramnivas | AI/ML Developer",
  description: "Portfolio of Attanti Ramnivas - AI/ML Developer & B.Tech CSBS Student at Jain University, Bengaluru",
  keywords: ["AI", "ML", "Developer", "Portfolio", "Machine Learning", "Jain University"],
  authors: [{ name: "Attanti Ramnivas" }],
  openGraph: {
    title: "Attanti Ramnivas | AI/ML Developer",
    description: "AI/ML Developer & B.Tech CSBS Student building the future with AI",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className="antialiased bg-[#030014] min-h-screen text-gray-100 font-sans">
        {children}
      </body>
    </html>
  );
}
