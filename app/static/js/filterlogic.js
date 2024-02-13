document.addEventListener('DOMContentLoaded', () => {
    createTagCheckboxes(tagData);
    updateSelectedNotes(); // Initial call to populate available notes with all note IDs
});
function createTagCheckboxes(tagData) {
    const container = document.getElementById('tagCheckboxes');
    Object.keys(tagData).forEach(tag => {
        const checkboxWrapper = document.createElement('div');
        checkboxWrapper.id = `wrapper_${tag}`;
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = tag;
        checkbox.value = tag;
        checkbox.addEventListener('change', updateSelectedNotes);
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
        container.appendChild(checkboxWrapper);
    });
}
function updateSelectedNotes() {
    const checkedTags = Array.from(document.querySelectorAll('input[type=checkbox]:checked')).map(checkbox => checkbox.id);
    const allNoteIds = new Set();
    Object.values(tagData).forEach(notes => notes.forEach(noteId => allNoteIds.add(noteId)));
    const sharedNoteIds = checkedTags.length > 0 ? getSharedNoteIds(checkedTags) : allNoteIds;
    updateAvailableNotesList(sharedNoteIds);
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
    if (countSpan)
        countSpan.textContent = ` (${noteCount})`;
    if (wrapper)
        wrapper.style.color = 'black';
    checkbox.disabled = false;
}
function setTagState(tag, noteCount, isEnabled) {
    const countSpan = document.getElementById(`count_${tag}`);
    const wrapper = document.getElementById(`wrapper_${tag}`);
    const checkbox = document.getElementById(tag);
    if (countSpan)
        countSpan.textContent = ` (${noteCount})`;
    wrapper.style.color = isEnabled ? 'black' : 'grey';
    checkbox.disabled = !isEnabled;
}
function updateAvailableNotesList(noteIds) {
    const listElement = document.getElementById('availableNotes');
    listElement.innerHTML = ''; // Clear existing list items
    noteIds.forEach(noteId => {
        const listItem = document.createElement('li');
        listItem.textContent = noteId.toString();
        listElement.appendChild(listItem);
    });
}
