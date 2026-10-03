"use client";

const orders = [
  { id: "ORD-001", customer: "Alice Johnson", date: "2024-01-15", amount: "$234.00", status: "Completed" },
  { id: "ORD-002", customer: "Bob Smith", date: "2024-01-14", amount: "$567.00", status: "Pending" },
  { id: "ORD-003", customer: "Carol White", date: "2024-01-14", amount: "$123.00", status: "Completed" },
  { id: "ORD-004", customer: "David Brown", date: "2024-01-13", amount: "$890.00", status: "Processing" },
  { id: "ORD-005", customer: "Eve Davis", date: "2024-01-13", amount: "$456.00", status: "Completed" },
];

const statusColors: Record<string, string> = {
  Completed: "bg-green-500/20 text-green-400",
  Pending: "bg-yellow-500/20 text-yellow-400",
  Processing: "bg-blue-500/20 text-blue-400",
  Cancelled: "bg-red-500/20 text-red-400",
};

export default function DataTable() {
  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="border-b border-gray-800">
            <th className="text-left text-xs font-medium text-gray-400 uppercase tracking-wider pb-3">
              Order ID
            </th>
            <th className="text-left text-xs font-medium text-gray-400 uppercase tracking-wider pb-3">
              Customer
            </th>
            <th className="text-left text-xs font-medium text-gray-400 uppercase tracking-wider pb-3">
              Date
            </th>
            <th className="text-left text-xs font-medium text-gray-400 uppercase tracking-wider pb-3">
              Amount
            </th>
            <th className="text-left text-xs font-medium text-gray-400 uppercase tracking-wider pb-3">
              Status
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-800">
          {orders.map((order) => (
            <tr key={order.id} className="hover:bg-gray-800/50 transition-colors">
              <td className="py-4 text-sm font-medium text-white">{order.id}</td>
              <td className="py-4 text-sm text-gray-300">{order.customer}</td>
              <td className="py-4 text-sm text-gray-400">{order.date}</td>
              <td className="py-4 text-sm font-medium text-white">{order.amount}</td>
              <td className="py-4">
                <span
                  className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                    statusColors[order.status]
                  }`}
                >
                  {order.status}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
