"use client";

import { useState } from "react";
import ProductCard from "./ProductCard";
import { Product } from "@/context/CartContext";

const products: Product[] = [
  {
    id: "1",
    name: "Premium Wireless Headphones",
    price: 299.99,
    image: "🎧",
    category: "Electronics",
    description: "High-quality wireless headphones with noise cancellation",
  },
  {
    id: "2",
    name: "Smart Watch Pro",
    price: 449.99,
    image: "⌚",
    category: "Electronics",
    description: "Advanced smartwatch with health monitoring features",
  },
  {
    id: "3",
    name: "Leather Messenger Bag",
    price: 189.99,
    image: "👜",
    category: "Fashion",
    description: "Handcrafted genuine leather messenger bag",
  },
  {
    id: "4",
    name: "Running Shoes Ultra",
    price: 159.99,
    image: "👟",
    category: "Sports",
    description: "Lightweight running shoes for maximum performance",
  },
  {
    id: "5",
    name: "Mechanical Keyboard",
    price: 179.99,
    image: "⌨️",
    category: "Electronics",
    description: "RGB mechanical keyboard with Cherry MX switches",
  },
  {
    id: "6",
    name: "Ceramic Coffee Set",
    price: 79.99,
    image: "☕",
    category: "Home",
    description: "Premium ceramic coffee set for 4 people",
  },
  {
    id: "7",
    name: "Polarized Sunglasses",
    price: 129.99,
    image: "🕶️",
    category: "Fashion",
    description: "Stylish polarized sunglasses with UV protection",
  },
  {
    id: "8",
    name: "Yoga Mat Premium",
    price: 89.99,
    image: "🧘",
    category: "Sports",
    description: "Non-slip yoga mat with carrying strap",
  },
];

const categories = ["All", "Electronics", "Fashion", "Sports", "Home"];

export default function ProductList() {
  const [activeCategory, setActiveCategory] = useState("All");

  const filteredProducts =
    activeCategory === "All"
      ? products
      : products.filter((p) => p.category === activeCategory);

  return (
    <div>
      {/* Category Filter */}
      <div className="flex flex-wrap justify-center gap-3 mb-12">
        {categories.map((category) => (
          <button
            key={category}
            onClick={() => setActiveCategory(category)}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
              activeCategory === category
                ? "bg-blue-600 text-white"
                : "bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-white"
            }`}
          >
            {category}
          </button>
        ))}
      </div>

      {/* Products Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {filteredProducts.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
}
