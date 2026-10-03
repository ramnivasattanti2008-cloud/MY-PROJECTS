import type { Metadata } from "next";
import "./globals.css";
import Navbar from "@/components/Navbar";
import CartProvider from "@/context/CartContext";

export const metadata: Metadata = {
  title: "ShopStore - E-Commerce Template",
  description: "A modern e-commerce template built with Next.js 15 and Tailwind CSS",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="bg-gray-950 text-gray-100 antialiased">
        <CartProvider>
          <Navbar />
          {children}
        </CartProvider>
      </body>
    </html>
  );
}
