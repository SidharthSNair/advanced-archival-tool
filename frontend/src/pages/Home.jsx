// import { useState } from "react";
// import RegionSelector from "../components/RegionSelector";
// import FileTree from "../components/FileTree";
//
// export default function Home() {
//   const [selectedShare, setSelectedShare] = useState(null);
//   const [region, setRegion] = useState(null);
//   const [location, setLocation] = useState(null);
//
//   // When RegionSelector sends data
//   const handleSelection = ({ share, region, location }) => {
//     setSelectedShare(share);
//     setRegion(region);
//     setLocation(location);
//   };
//
//   return (
//     <div className="max-w-6xl mx-auto p-6 space-y-6">
//       <h1 className="text-2xl font-bold mb-2">File Share Browser</h1>
//       <RegionSelector onShareSelect={handleSelection} />
//
//       {selectedShare && (
//         <>
//           <div className="mt-6 border-t pt-4">
//             <h2 className="text-xl font-semibold mb-3">
//               Browsing: {selectedShare.unc_path}
//             </h2>
//             <FileTree
//               share={selectedShare}
//               regionCode={region}
//               locationCode={location}
//             />
//           </div>
//         </>
//       )}
//     </div>
//   );
// }

//Second Version

import { useState } from "react";
import RegionSelector from "../components/RegionSelector";
import FiltersBar from "../components/FiltersBar";
import FileTree from "../components/FileTree";

export default function Home() {
  const [selection, setSelection] = useState(null); // { share, region, location }
  const [filters, setFilters] = useState({ q: "", kind: "all" });

  // const handleSelect = ({ share, region, location }) => setSelection({ share, region, location });

  const handleSelect = ({ share, region, location }) => {
    setSelection({ share, region, location });
    setFilters({ q: "", kind: "all" });
    }

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold">File Share Browser</h1>
      <RegionSelector onShareSelect={handleSelect} />

      {selection?.share && (
        <>
          <FiltersBar onChange={setFilters} />

          <div className="mt-4 border-t pt-4">
            <h2 className="text-xl font-semibold mb-3">Browsing: {selection.share.unc_path}</h2>
            <FileTree
              key={selection.share.id}
              share={selection.share}
              regionCode={selection.region}
              locationCode={selection.location}
              filters={filters}
              filters={filters}
            />
          </div>
        </>
      )}
    </div>
  );
}


