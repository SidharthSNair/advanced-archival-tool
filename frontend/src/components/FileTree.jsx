// import { useState } from "react";
// import Tree from "rc-tree";
// import { fetchNodes } from "../api/nodes";
// import { scheduleArchive } from "../api/archive";
//
// export default function FileTree({ share, regionCode, locationCode }){
//   const [treeData, setTreeData] = useState([]);
//   const [selectedKeys, setSelectedKeys] = useState([]);
//   const [checkedNodes, setCheckedNodes] = useState([]);
//
//   // Load root nodes (initial load)
//   const loadRoot = async () => {
//     const data = await fetchNodes(share.id);
//     setTreeData(convertToTree(data));
//   };
//
//   // Lazy load children when expanding
//   const onLoadData = async (treeNode) => {
//     const { id } = treeNode;
//     const data = await fetchNodes(share.id, id);
//     const children = convertToTree(data);
//
//     setTreeData((origin) =>
//       updateTreeData(origin, treeNode.key, children)
//     );
//   };
//
//   // Helper: convert API nodes → rc-tree format
//   const convertToTree = (nodes) =>
//     nodes.map((n) => ({
//       title: n.name,
//       key: n.id,
//       id: n.id,
//       isLeaf: !n.is_dir,
//     }));
//
//   // Helper: recursively update children in treeData
//   function updateTreeData(list, key, children) {
//     return list.map((node) => {
//       if (node.key === key) {
//         return { ...node, children };
//       }
//       if (node.children) {
//         return {
//           ...node,
//           children: updateTreeData(node.children, key, children),
//         };
//       }
//       return node;
//     });
//   }
//
//   const handleCheck = (checkedKeys, { checkedNodes }) => {
//     setSelectedKeys(checkedKeys);
//     setCheckedNodes(checkedNodes);
//   };
//
//   // Load on first render (lazy)
//   if (treeData.length === 0) {
//     loadRoot();
//   }
//
//   const handleSchedule = async () => {
//   const paths = checkedNodes.map((n) => n.title);
//   if (paths.length === 0) {
//     alert("No files or folders selected!");
//     return;
//   }
//
//     try {
//     const res = await scheduleArchive(regionCode, locationCode, share, paths);
//     alert(`✅ Archive scheduled for ${new Date(res.scheduled_for).toLocaleString()}`);
//   } catch (err) {
//     alert(`❌ Failed to schedule: ${err.message}`);
//   }
// };
//
//   return (
//     <div className="flex space-x-4 mt-6">
//       <div className="flex-1 border rounded bg-white p-2 overflow-auto h-[70vh]">
//         <Tree
//           checkable
//           loadData={onLoadData}
//           treeData={treeData}
//           onCheck={handleCheck}
//         />
//       </div>
//
//       <div className="w-1/3 bg-white p-3 border rounded h-[70vh] overflow-auto flex flex-col">
//         <h3 className="text-lg font-semibold mb-2">Selected Items</h3>
//         {checkedNodes.length === 0 ? (
//           <p className="text-gray-500 text-sm">No items selected</p>
//         ) : (
//           <ul className="text-sm list-disc pl-5 flex-1 overflow-auto">
//             {checkedNodes.map((n) => (
//               <li key={n.key}>{n.title}</li>
//             ))}
//           </ul>
//         )}
//
//         <button
//           onClick={handleSchedule}
//           className="mt-4 bg-blue-600 text-white rounded py-2 hover:bg-blue-700 transition"
//         >
//           Schedule Archive
//         </button>
//       </div>
//     </div>
//     );
//   }

// Second version

// import { useState, useEffect } from "react";
// import Tree from "rc-tree";
// import { fetchNodes } from "../api/nodes";
// import { scheduleArchive } from "../api/archive";
//
// export default function FileTree({ share, regionCode, locationCode }) {
//   const [treeData, setTreeData] = useState([]);
//   const [checkedNodes, setCheckedNodes] = useState([]);
//
//   // ✅ Load root nodes once when component mounts
//   useEffect(() => {
//     if (share?.id) loadRoot();
//   }, [share]);
//
//   // Load root nodes (initial load)
//   const loadRoot = async () => {
//     const data = await fetchNodes(share.id);
//     setTreeData(convertToTree(data));
//   };
//
//   // Lazy load children when expanding
//   const onLoadData = async (treeNode) => {
//     const { id } = treeNode;
//     const data = await fetchNodes(share.id, id);
//     const children = convertToTree(data);
//
//     setTreeData((origin) => updateTreeData(origin, treeNode.key, children));
//   };
//
//   // ✅ Convert API nodes → rc-tree format (include full path)
//   const convertToTree = (nodes) =>
//     nodes.map((n) => ({
//       title: n.name,
//       key: n.id,
//       id: n.id,
//       path: n.path, // ✅ include full relative path like "hr/policy.txt"
//       isLeaf: !n.is_dir,
//     }));
//
//   // Helper: recursively update children in treeData
//   function updateTreeData(list, key, children) {
//     return list.map((node) => {
//       if (node.key === key) {
//         return { ...node, children };
//       }
//       if (node.children) {
//         return {
//           ...node,
//           children: updateTreeData(node.children, key, children),
//         };
//       }
//       return node;
//     });
//   }
//
//   // Handle selection
//    const handleCheck = (checkedKeys, { checkedNodes }) => {
//      setCheckedNodes(checkedNodes);
//    };
//
//
//   // ✅ Updated handleSchedule
//   const handleSchedule = async () => {
//     if (checkedNodes.length === 0) {
//       alert("No files or folders selected!");
//       return;
//     }
//
//     // ✅ Build full UNC paths for backend
//     const paths = checkedNodes.map((n) => {
//       const relative = n.path?.replace(/\//g, "\\") || n.title;
//       // return `${share.unc_path}\\${relative}`;
//       return relative;
//     });
//
//     try {
//       const res = await scheduleArchive(regionCode, locationCode, share, paths);
//       alert(`✅ Archive scheduled for ${new Date(res.scheduled_for).toLocaleString()}`);
//     } catch (err) {
//       alert(`❌ Failed to schedule: ${err.message}`);
//     }
//   };
//
//   return (
//     <div className="flex space-x-4 mt-6">
//       {/* File tree */}
//       <div className="flex-1 border rounded bg-white p-2 overflow-auto h-[70vh]">
//         <Tree
//           checkable
//           loadData={onLoadData}
//           treeData={treeData}
//           onCheck={handleCheck}
//         />
//       </div>
//
//       {/* Selected items */}
//       <div className="w-1/3 bg-white p-3 border rounded h-[70vh] overflow-auto flex flex-col">
//         <h3 className="text-lg font-semibold mb-2">Selected Items</h3>
//
//         {checkedNodes.length === 0 ? (
//           <p className="text-gray-500 text-sm">No items selected</p>
//         ) : (
//           <ul className="text-sm list-disc pl-5 flex-1 overflow-auto">
//             {checkedNodes.map((n) => (
//               <li key={n.key}>{n.path || n.title}</li>
//             ))}
//           </ul>
//         )}
//
//         <button
//           onClick={handleSchedule}
//           className="mt-4 bg-blue-600 text-white rounded py-2 hover:bg-blue-700 transition"
//         >
//           Schedule Archive
//         </button>
//       </div>
//     </div>
//   );
// }

// Third Version

import { useEffect, useState } from "react";
import Tree from "rc-tree";
import { fetchNodesPaged } from "../api/nodes";
import ReviewModal from "./ReviewModal";
import { scheduleArchive } from "../api/archive";

const LOAD_MORE_PREFIX = "loadmore";

export default function FileTree({ share, regionCode, locationCode, filters }) {
  const [treeData, setTreeData] = useState([]);
  const [checkedNodes, setCheckedNodes] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [expandedKeys, setExpandedKeys] = useState([]);


  // Build rc-tree nodes
//   const toTreeNodes = (items) =>
//     items.map((n) => ({
//       title: n.name,
//       key: String(n.id),
//       id: n.id,
//       isLeaf: n.is_dir ? false : true,
//       path: n.path,
//     }));

  // Build rc-tree nodes
  const toTreeNodes = (items) =>
    items.map((n) => {
      // ✅ compute days since modified
      let label = "";
      if (n.modified_at) {
        const modifiedDate = new Date(n.modified_at);
        const now = new Date();
        const diffMs = now - modifiedDate;
        const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
        label = diffDays === 0
          ? "(today)"
          : diffDays === 1
          ? "(1 day ago)"
          : `(${diffDays} days ago)`;
      }

      return {
        title: (
          <span className="flex items-center gap-2">
            <span className={n.is_dir ? "font-semibold text-yellow-700" : "text-gray-800"}>
              {n.name}
            </span>
            <span className="text-xs text-gray-500 ml-1 italic">{label}</span>
          </span>
        ),
        key: String(n.id),
        id: n.id,
        isLeaf: !n.is_dir,
        path: n.path,
      };
    });


  // Add a "Load more..." pseudo-node
  const loadMoreNode = (parentKey, nextOffset) => ({
    title: "Load more…",
    key: `${LOAD_MORE_PREFIX}:${parentKey}:${nextOffset}`,
    isLeaf: true,
    disabled: false,
    selectable: false,
    className: "italic text-gray-500",
  });

  // Replace/merge children under a parent
  function updateChildren(list, parentKey, newChildren, append = false) {
    return list.map((n) => {
      if (n.key === parentKey) {
        const merged = append && n.children ? [...n.children, ...newChildren] : newChildren;
        return { ...n, children: merged };
      }
      if (n.children) return { ...n, children: updateChildren(n.children, parentKey, newChildren, append) };
      return n;
    });
  }

  // Load root using filters
//   const loadRoot = async () => {
//     const { items, next_offset } = await fetchNodesPaged({
//       shareId: share.id, parentId: null, q: filters.q, kind: filters.kind,
//     });
//     let nodes = toTreeNodes(items);
//     if (next_offset !== null) nodes = [...nodes, loadMoreNode("root", next_offset)];
//     setTreeData(nodes);
//   };

  const loadRoot = async () => {
    const { items, next_offset } = await fetchNodesPaged({
      shareId: share.id,
      parentId: null,
      q: filters.q,
      kind: filters.kind,
      days: filters.days,
    });
    console.log("API returned:", { items, next_offset });   // 👈 add this
    let nodes = toTreeNodes(items);
    console.log("Converted tree nodes:", nodes);             // 👈 add this
    if (next_offset !== null) nodes = [...nodes, loadMoreNode("root", next_offset)];
    setTreeData(nodes);
  };


  // Lazy load children or handle "load more"
  //   const onLoadData = async (treeNode) => {
  //     const key = treeNode.key;
  //
  //     // If it's a 'load more' pseudo node, parse it and fetch next page
  //     if (key.startsWith(`${LOAD_MORE_PREFIX}:`)) {
  //       const [_p, parentKey, nextOffsetStr] = key.split(":");
  //       const parentId = parentKey === "root" ? null : Number(parentKey);
  //       const { items, next_offset } = await fetchNodesPaged({
  //         shareId: share.id, parentId, offset: Number(nextOffsetStr), q: filters.q, kind: filters.kind,
  //       });
  //
  //       let children = toTreeNodes(items);
  //       if (next_offset !== null) children = [...children, loadMoreNode(parentKey, next_offset)];
  //       setTreeData((orig) => updateChildren(orig, parentKey === "root" ? "root" : String(parentId), children, true));
  //       return;
  //     }
  //
  //     // Normal expansion: first-time load of children
  //     const parentId = Number(treeNode.id);
  //     const { items, next_offset } = await fetchNodesPaged({
  //       shareId: share.id, parentId, q: filters.q, kind: filters.kind,
  //     });
  //
  //     let children = toTreeNodes(items);
  //     if (next_offset !== null) children = [...children, loadMoreNode(String(parentId), next_offset)];
  //     setTreeData((orig) => updateChildren(orig, String(parentId), children));
  //   };

    const onLoadData = async (treeNode) => {
    const key = treeNode.key;

    // Handle "load more" pagination
    if (key.startsWith(`${LOAD_MORE_PREFIX}:`)) {
      const [_p, parentKey, nextOffsetStr] = key.split(":");
      const parentId = parentKey === "root" ? null : Number(parentKey);
      const { items, next_offset } = await fetchNodesPaged({
        shareId: share.id,
        parentId,
        offset: Number(nextOffsetStr),
        q: filters.q,
        kind: filters.kind,
        days: filters.days, // ✅ apply filters to pagination
      });

      let children = toTreeNodes(items);
      if (next_offset !== null)
        children = [...children, loadMoreNode(parentKey, next_offset)];
      setTreeData((orig) =>
        updateChildren(
          orig,
          parentKey === "root" ? "root" : String(parentId),
          children,
          true
        )
      );
      return;
    }

    // Normal expansion — fetch children for this parent
    const parentId = Number(treeNode.id);
    const { items, next_offset } = await fetchNodesPaged({
      shareId: share.id,
      parentId,
      q: filters.q,
      kind: filters.kind,
      days: filters.days, // ✅ important — same filters apply to children
    });

    let children = toTreeNodes(items);
    if (next_offset !== null)
      children = [...children, loadMoreNode(String(parentId), next_offset)];

    setTreeData((orig) => updateChildren(orig, String(parentId), children));
  };


  const handleCheck = (_checkedKeys, { checkedNodes }) => {
    setCheckedNodes(checkedNodes);
  };

  // Open review modal instead of scheduling immediately
  const openReview = () => {
    if (checkedNodes.length === 0) {
      alert("No files or folders selected!");
      return;
    }
    setModalOpen(true);
  };

  const confirmSchedule = async () => {
    const paths = checkedNodes.map((n) => n.path || n.title);
    try {
      const res = await scheduleArchive(regionCode, locationCode, share, paths);
      setModalOpen(false);
      alert(`✅ Scheduled for ${new Date(res.scheduled_for).toLocaleString()}`);
    } catch (e) {
      alert(`❌ Failed: ${e.message}`);
    }
  };

  // Reload root whenever share or filters change
  useEffect(() => {
    setTreeData([]);
    setCheckedNodes([]);
    setExpandedKeys([]);
    
    loadRoot();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [share?.id, filters.q, filters.kind, filters.days]);

  return (
    <>
      <div className="flex space-x-4 mt-6">
        <div className="flex-1 border rounded bg-white p-2 overflow-auto h-[70vh]">
          <Tree
            checkable
            loadData={onLoadData}
            treeData={treeData}
            expandedKeys={expandedKeys}
            onExpand={setExpandedKeys}
            onCheck={handleCheck}
          />
        </div>

        <div className="w-1/3 bg-white p-3 border rounded h-[70vh] overflow-auto flex flex-col">
          <h3 className="text-lg font-semibold mb-2">Selected Items</h3>
          {checkedNodes.length === 0 ? (
            <p className="text-gray-500 text-sm">No items selected</p>
          ) : (
            <ul className="text-sm list-disc pl-5 flex-1 overflow-auto">
              {checkedNodes.map((n) => (<li key={n.key} title={n.path}>{n.title}</li>))}
            </ul>
          )}
          <button
            onClick={openReview}
            className="mt-4 bg-blue-600 text-white rounded py-2 hover:bg-blue-700 transition"
          >
            Review & Schedule
          </button>
        </div>
      </div>

      <ReviewModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onConfirm={confirmSchedule}
        data={{
          regionCode,
          locationCode,
          share,
          paths: checkedNodes.map((n) => n.path || n.title),
        }}
      />
    </>
  );
}


