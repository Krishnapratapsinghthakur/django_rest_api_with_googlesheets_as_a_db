import './DeleteConfirm.css';

function DeleteConfirm({ isOpen, item, onClose, onConfirm, loading }) {
    if (!isOpen || !item) return null;

    return (
        <div className="delete-overlay" onClick={onClose}>
            <div className="delete-modal" onClick={(e) => e.stopPropagation()}>
                <div className="delete-icon">
                    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 9V13M12 17H12.01M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                </div>

                <h3>Delete Item?</h3>
                <p>Are you sure you want to delete <strong>"{item.name}"</strong>? This action cannot be undone.</p>

                <div className="delete-actions">
                    <button className="btn-cancel" onClick={onClose} disabled={loading}>
                        Cancel
                    </button>
                    <button className="btn-delete" onClick={() => onConfirm(item.id)} disabled={loading}>
                        {loading ? (
                            <>
                                <span className="btn-spinner"></span>
                                Deleting...
                            </>
                        ) : (
                            'Delete'
                        )}
                    </button>
                </div>
            </div>
        </div>
    );
}

export default DeleteConfirm;
