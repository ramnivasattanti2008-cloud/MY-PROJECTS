"use client";

import { useState } from "react";
import ProductList from "@/components/ProductList";
import Cart from "@/components/Cart";
import Checkout from "@/components/Checkout";
import { ShoppingBag, X } from "lucide-react";
import { useCart } from "@/context/CartContext";

type View = "products" | "cart" | "checkout";

export default function Home() {
  const [currentView, setCurrentView] = useState<View>("products");
  const { cartCount } = useCart();

  return (
    <main className="min-h-screen pt-20 pb-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {currentView === "products" && (
          <>
            <div className="text-center mb-12">
              <h1 className="text-4xl font-bold text-white mb-4">
                Featured Products
              </h1>
              <p className="text-gray-400 max-w-2xl mx-auto">
                Discover our curated selection of premium products
              </p>
            </div>
            <ProductList />
          </>
        )}
        {currentView === "cart" && <Cart onContinueShopping={() => setCurrentView("products")} onCheckout={() => setCurrentView("checkout")} />}
        {currentView === "checkout" && <Checkout onBack={() => setCurrentView("cart")} onComplete={() => setCurrentView("products")} />}
      </div>

      {/* Floating Cart Button */}
      {currentView === "products" && (
        <button
          onClick={() => setCurrentView("cart")}
          className="fixed bottom-6 right-6 bg-blue-600 hover:bg-blue-700 text-white p-4 rounded-full shadow-lg flex items-center gap-2 transition-all transform hover:scale-105 z-40"
        >
          <ShoppingBag className="w-6 h-6" />
          {cartCount > 0 && (
            <span className="absolute -top-2 -right-2 bg-red-500 text-white text-sm font-bold w-6 h-6 rounded-full flex items-center justify-center">
              {cartCount}
            </span>
          )}
        </button>
      )}
    </main>
  );
}
