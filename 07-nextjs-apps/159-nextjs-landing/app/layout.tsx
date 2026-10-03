import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "NextJS Landing - Modern Landing Page",
  description: "A modern landing page template built with Next.js 15 and Tailwind CSS",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="bg-gray-950 text-gray-100 antialiased">
        {children}
      </body>
    </html>
  );
}
