# NextJS E-Commerce Template

A modern, dark-themed e-commerce template built with Next.js 15, TypeScript, Tailwind CSS, and Lucide icons.

## Features

- Product listing with category filtering
- Shopping cart with add/remove/update quantity
- Multi-step checkout flow (Shipping > Payment > Confirmation)
- Cart context with React Context API
- Responsive dark theme design
- Product cards with hover effects

## Tech Stack

- **Framework:** Next.js 15 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Icons:** Lucide React
- **State:** React Context API
- **Theme:** Dark mode

## Getting Started

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## Project Structure

```
nextjs-ecommerce/
├── app/
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── Navbar.tsx
│   ├── ProductList.tsx
│   ├── ProductCard.tsx
│   ├── Cart.tsx
│   └── Checkout.tsx
├── context/
│   └── CartContext.tsx
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── README.md
```

## Features

### Product Listing
- Grid layout with responsive design
- Category filter buttons
- Product cards with image, title, price, and add to cart button

### Shopping Cart
- View cart contents
- Update item quantities
- Remove items
- Order summary with total

### Checkout Flow
1. **Shipping Information** - Collect customer details
2. **Payment Information** - Collect payment method
3. **Order Confirmation** - Success message

### Cart Context
- Global state management for cart
- Add, remove, update quantities
- Cart total and count calculations

## Cart Context API

```typescript
interface CartContextType {
  cart: CartItem[];
  addToCart: (product: Product) => void;
  removeFromCart: (id: string) => void;
  updateQuantity: (id: string, quantity: number) => void;
  clearCart: () => void;
  cartTotal: number;
  cartCount: number;
}
```

## Customization

1. Update products in `components/ProductList.tsx`
2. Modify cart styling and layout
3. Add real payment integration
4. Connect to backend API

## License

MIT
