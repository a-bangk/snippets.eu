document.addEventListener('DOMContentLoaded', () => {
    const pathSegments = window.location.pathname.split('/');
    const urlTag = pathSegments[pathSegments.length - 1]; 
    let tagOnly = urlTag.split('=')[1];
    tagFromUrl=decodeURIComponent(tagOnly);
    console.log("tagFromUrl: ",tagFromUrl)
    createTagCheckboxes(tagData, tagFromUrl);
    updateSelectedNotes();
});
window.addEventListener('beforeunload', function (event) {
    localStorage.clear();
});

function createTagCheckboxes(tagData, tagFromUrl) {
    console.log(tagData, tagFromUrl)
    const container = document.getElementById('tagCheckboxes');
    Object.keys(tagData).forEach(tag => {
        const checkboxWrapper = document.createElement('div');
        checkboxWrapper.id = `wrapper_${tag}`;
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = tag;
        checkbox.value = tag;
        const checkedTags = JSON.parse(localStorage.getItem('checkedTags') || '[]');
        if (checkedTags.includes(tag)|| tag === tagFromUrl) {
            checkbox.checked = true;        }
        checkbox.addEventListener('change', () => {
            updateSelectedNotes();
            saveCheckedState();
        });
        const label = document.createElement('label');
        label.htmlFor = tag;
        label.textContent = tag;
        const countSpan = document.createElement('span');
        countSpan.id = `count_${tag}`;
        countSpan.textContent = ` (${tagData[tag].length})`;
        countSpan.style.marginLeft = '10px';
        label.appendChild(countSpan);
        checkboxWrapper.appendChild(checkbox);
        checkboxWrapper.appendChild(label);
        if (tag === tagFromUrl) {
            checkboxWrapper.classList.add('hidden'); }
        container.appendChild(checkboxWrapper);
    });
}

function saveCheckedState() {
    const allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
    const checkedTags = Array.from(allCheckboxes).filter(checkbox => checkbox.checked).map(checkbox => checkbox.id);
    localStorage.setItem('checkedTags', JSON.stringify(checkedTags));
}

function updateSelectedNotes() {
    const checkedTags = Array.from(document.querySelectorAll('input[type=checkbox]:checked')).map(checkbox => checkbox.id);
    const allNoteIds = new Set();
    Object.values(tagData).forEach(notes => notes.forEach(noteId => allNoteIds.add(noteId)));
    const sharedNoteIds = checkedTags.length > 0 ? getSharedNoteIds(checkedTags) : allNoteIds;
    if (checkedTags.length === 0) {
        Object.keys(tagData).forEach(tag => resetTagState(tag, tagData[tag].length));
    }
    else {
        Object.keys(tagData).forEach(tag => {
            const uniqueNotesCount = tagData[tag].filter(noteId => sharedNoteIds.has(noteId)).length;
            const isEnabled = uniqueNotesCount > 0;
            setTagState(tag, uniqueNotesCount, isEnabled);
        });
    }
    console.log(sharedNoteIds)
    document.getElementById('noteIdsField').value = JSON.stringify(Array.from(sharedNoteIds));
}

function getSharedNoteIds(checkedTags) {
    return checkedTags.reduce((sharedIds, tag, index) => {
        const noteIds = new Set(tagData[tag]);
        if (index === 0) {
            return noteIds;
        }
        return new Set([...sharedIds].filter(id => noteIds.has(id)));
    }, new Set());
}

function resetTagState(tag, noteCount) {
    const countSpan = document.getElementById(`count_${tag}`);
    const wrapper = document.getElementById(`wrapper_${tag}`);
    const checkbox = document.getElementById(tag);
    // Reset text content for the countSpan
    if (countSpan) {
        countSpan.textContent = ` (${noteCount})`;
        countSpan.style.display = ""; // Ensure it is visible
    }
    // Ensure the wrapper and checkbox are visible
    if (wrapper) {
        wrapper.style.display = ""; // Reset display to default or use 'block', 'inline', etc., as needed
    }
    if (checkbox) {
        checkbox.style.display = ""; // Reset display to default or use 'inline-block' for checkboxes
        checkbox.disabled = false; // Ensure checkbox is enabled
    }
}

function setTagState(tag, noteCount, isEnabled) {
    const countSpan = document.getElementById(`count_${tag}`);
    const wrapper = document.getElementById(`wrapper_${tag}`);
    const checkbox = document.getElementById(tag);
    if (isEnabled) {
        // Show elements if they are enabled
        if (countSpan) countSpan.style.display = ""; // Reset to default or you can use 'inline' or 'block' depending on your layout
        if (wrapper) wrapper.style.display = ""; // Reset to default or use 'block', 'inline', etc.
        if (checkbox) checkbox.style.display = ""; // Reset to default or use 'inline-block' for checkboxes
        if (countSpan) countSpan.textContent = ` (${noteCount})`; // Update note count when enabled
    } else {
        // Hide elements if they are not enabled
        if (countSpan) countSpan.style.display = "none";
        if (wrapper) wrapper.style.display = "none";
        if (checkbox) checkbox.style.display = "none";
    }
}

function setTagStateOld(tag, noteCount, isEnabled) {
    const countSpan = document.getElementById(`count_${tag}`);
    const wrapper = document.getElementById(`wrapper_${tag}`);
    const checkbox = document.getElementById(tag);
    if (countSpan)
        countSpan.textContent = ` (${noteCount})`;
    wrapper.style.color = isEnabled ? 'black' : 'grey';
    checkbox.disabled = !isEnabled;
}