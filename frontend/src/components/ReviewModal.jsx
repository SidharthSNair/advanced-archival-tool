export default function ReviewModal({ open, onClose, onConfirm, data }) {
  if (!open) return null;
  const { regionCode, locationCode, share, paths } = data || {};
  const shown = (paths || []).slice(0, 10);

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-xl p-5">
        <h3 className="text-xl font-semibold mb-2">Confirm Archive</h3>
        <p className="text-sm text-gray-600 mb-3">
          Region: <b>{regionCode}</b> · Location: <b>{locationCode}</b> · Share: <b>{share?.unc_path}</b>
        </p>
        <p className="text-sm mb-2">Selected items: <b>{paths?.length || 0}</b></p>
        <ul className="text-xs max-h-60 overflow-auto border rounded p-2 bg-gray-50">
          {shown.map((p, i) => (<li key={i} className="truncate">{p}</li>))}
          {paths && paths.length > 10 && <li className="text-gray-500">…and {paths.length - 10} more</li>}
        </ul>

        <div className="mt-5 flex justify-end gap-2">
          <button className="px-4 py-2 rounded border" onClick={onClose}>Cancel</button>
          <button className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700" onClick={onConfirm}>
            Schedule
          </button>
        </div>
      </div>
    </div>
  );
}
