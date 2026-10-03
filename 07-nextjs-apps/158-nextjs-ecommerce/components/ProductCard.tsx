"use client";

import { Plus, Heart } from "lucide-react";
import { Product, useCart } from "@/context/CartContext";

interface ProductCardProps {
  product: Product;
}

export default function ProductCard({ product }: ProductCardProps) {
  const { addToCart } = useCart();

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden group hover:border-gray-700 transition-colors">
      <div className="relative h-48 bg-gray-800 flex items-center justify-center">
        <span className="text-6xl">{product.image}</span>
        <button className="absolute top-3 right-3 p-2 bg-gray-900/80 rounded-full text-gray-400 hover:text-white transition-colors opacity-0 group-hover:opacity-100">
          <Heart className="w-4 h-4" />
        </button>
      </div>
      <div className="p-4">
        <span className="text-xs text-blue-400 font-medium">{product.category}</span>
        <h3 className="text-white font-semibold mt-1 mb-2">{product.name}</h3>
        <p className="text-gray-400 text-sm mb-4 line-clamp-2">{product.description}</p>
        <div className="flex items-center justify-between">
          <span className="text-xl font-bold text-white">${product.price}</span>
          <button
            onClick={() => addToCart(product)}
            className="bg-blue-600 hover:bg-blue-700 text-white p-2 rounded-lg transition-colors"
          >
            <Plus className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}
