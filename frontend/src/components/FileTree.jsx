import { useState } from "react";
import Tree from "rc-tree";
import { fetchNodes } from "../api/nodes";
import { scheduleArchive } from "../api/archive";

export default function FileTree({ share, regionCode, locationCode }){
  const [treeData, setTreeData] = useState([]);
  const [selectedKeys, setSelectedKeys] = useState([]);
  const [checkedNodes, setCheckedNodes] = useState([]);

  // Load root nodes (initial load)
  const loadRoot = async () => {
    const data = await fetchNodes(share.id);
    setTreeData(convertToTree(data));
  };

  // Lazy load children when expanding
  const onLoadData = async (treeNode) => {
    const { id } = treeNode;
    const data = await fetchNodes(share.id, id);
    const children = convertToTree(data);

    setTreeData((origin) =>
      updateTreeData(origin, treeNode.key, children)
    );
  };

  // Helper: convert API nodes → rc-tree format
  const convertToTree = (nodes) =>
    nodes.map((n) => ({
      title: n.name,
      key: n.id,
      id: n.id,
      isLeaf: !n.is_dir,
    }));

  // Helper: recursively update children in treeData
  function updateTreeData(list, key, children) {
    return list.map((node) => {
      if (node.key === key) {
        return { ...node, children };
      }
      if (node.children) {
        return {
          ...node,
          children: updateTreeData(node.children, key, children),
        };
      }
      return node;
    });
  }

  const handleCheck = (checkedKeys, { checkedNodes }) => {
    setSelectedKeys(checkedKeys);
    setCheckedNodes(checkedNodes);
  };

  // Load on first render (lazy)
  if (treeData.length === 0) {
    loadRoot();
  }

  const handleSchedule = async () => {
  const paths = checkedNodes.map((n) => n.title);
  if (paths.length === 0) {
    alert("No files or folders selected!");
    return;
  }

    try {
    const res = await scheduleArchive(regionCode, locationCode, share, paths);
    alert(`✅ Archive scheduled for ${new Date(res.scheduled_for).toLocaleString()}`);
  } catch (err) {
    alert(`❌ Failed to schedule: ${err.message}`);
  }
};

  return (
    <div className="flex space-x-4 mt-6">
      <div className="flex-1 border rounded bg-white p-2 overflow-auto h-[70vh]">
        <Tree
          checkable
          loadData={onLoadData}
          treeData={treeData}
          onCheck={handleCheck}
        />
      </div>

      <div className="w-1/3 bg-white p-3 border rounded h-[70vh] overflow-auto flex flex-col">
        <h3 className="text-lg font-semibold mb-2">Selected Items</h3>
        {checkedNodes.length === 0 ? (
          <p className="text-gray-500 text-sm">No items selected</p>
        ) : (
          <ul className="text-sm list-disc pl-5 flex-1 overflow-auto">
            {checkedNodes.map((n) => (
              <li key={n.key}>{n.title}</li>
            ))}
          </ul>
        )}

        <button
          onClick={handleSchedule}
          className="mt-4 bg-blue-600 text-white rounded py-2 hover:bg-blue-700 transition"
        >
          Schedule Archive
        </button>
      </div>
    </div>
    );
  }
