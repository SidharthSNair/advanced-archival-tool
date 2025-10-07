import { useState } from "react";
import RegionSelector from "../components/RegionSelector";
import FileTree from "../components/FileTree";

export default function Home() {
  const [selectedShare, setSelectedShare] = useState(null);
  const [region, setRegion] = useState(null);
  const [location, setLocation] = useState(null);

  // When RegionSelector sends data
  const handleSelection = ({ share, region, location }) => {
    setSelectedShare(share);
    setRegion(region);
    setLocation(location);
  };

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold mb-2">File Share Browser</h1>
      <RegionSelector onShareSelect={handleSelection} />

      {selectedShare && (
        <>
          <div className="mt-6 border-t pt-4">
            <h2 className="text-xl font-semibold mb-3">
              Browsing: {selectedShare.unc_path}
            </h2>
            <FileTree
              share={selectedShare}
              regionCode={region}
              locationCode={location}
            />
          </div>
        </>
      )}
    </div>
  );
}
