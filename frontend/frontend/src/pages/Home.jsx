import { useState } from "react";
import RegionSelector from "../components/RegionSelector";

export default function Home() {
  const [selectedShare, setSelectedShare] = useState(null);

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">File Share Browser</h1>
      <RegionSelector onShareSelect={setSelectedShare} />

      {selectedShare && (
        <div className="mt-6 p-4 bg-green-50 border rounded">
          <p>
            Selected Share: <strong>{selectedShare.unc_path}</strong>
          </p>
        </div>
      )}
    </div>
  );
}
