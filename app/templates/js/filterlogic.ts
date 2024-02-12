type TagNoteMapping = {
    [key: string]: number[];
};

const tagData: TagNoteMapping = {
    'tag 1': [245],
    'tag 2': [245, 246],
    'tag 3': [246],
    'tag 4': [248, 245]
};

document.addEventListener('DOMContentLoaded', () => {
    createTagCheckboxes(tagData);
    updateSelectedNotes(); // Initial call to populate available notes with all note IDs
});

function createTagCheckboxes(tagData: TagNoteMapping): void {
    const container = document.getElementById('tagCheckboxes') as HTMLElement;

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
        countSpan.textContent = ` (${tagData[tag].length} notes)`;
        countSpan.style.marginLeft = '10px';

        label.appendChild(countSpan);
        checkboxWrapper.appendChild(checkbox);
        checkboxWrapper.appendChild(label);
        container.appendChild(checkboxWrapper);
    });
}

function updateSelectedNotes(): void {
    const checkedTags = Array.from(document.querySelectorAll('input[type=checkbox]:checked')).map(checkbox => checkbox.id);

    const allNoteIds = new Set<number>();
    Object.values(tagData).forEach(notes => notes.forEach(noteId => allNoteIds.add(noteId)));
    const sharedNoteIds = checkedTags.length > 0 ? getSharedNoteIds(checkedTags) : allNoteIds;

    updateAvailableNotesList(sharedNoteIds);

    if (checkedTags.length === 0) {
        Object.keys(tagData).forEach(tag => resetTagState(tag, tagData[tag].length));
    } else {
        Object.keys(tagData).forEach(tag => {
            const uniqueNotesCount = tagData[tag].filter(noteId => sharedNoteIds.has(noteId)).length;
            const isEnabled = uniqueNotesCount > 0;
            setTagState(tag, uniqueNotesCount, isEnabled);
        });
    }
}

function getSharedNoteIds(checkedTags: string[]): Set<number> {
    return checkedTags.reduce((sharedIds, tag, index) => {
        const noteIds = new Set(tagData[tag]);
        if (index === 0) {
            return noteIds;
        }
        return new Set([...sharedIds].filter(id => noteIds.has(id)));
    }, new Set<number>());
}

function resetTagState(tag: string, noteCount: number): void {
    const countSpan = document.getElementById(`count_${tag}`);
    const wrapper = document.getElementById(`wrapper_${tag}`);
    const checkbox = document.getElementById(tag) as HTMLInputElement;

    if (countSpan) countSpan.textContent = ` (${noteCount} notes)`;
    if (wrapper) wrapper.style.color = 'black';
    checkbox.disabled = false;
}

function setTagState(tag: string, noteCount: number, isEnabled: boolean): void {
    const countSpan = document.getElementById(`count_${tag}`);
    const wrapper = document.getElementById(`wrapper_${tag}`);
    const checkbox = document.getElementById(tag) as HTMLInputElement;

    if (countSpan) countSpan.textContent = ` (${noteCount} unique note${noteCount !== 1 ? 's' : ''})`;
    wrapper.style.color = isEnabled ? 'black' : 'grey';
    checkbox.disabled = !isEnabled;
}

function updateAvailableNotesList(noteIds: Set<number>): void {
    const listElement = document.getElementById('availableNotes') as HTMLUListElement;
    listElement.innerHTML = ''; // Clear existing list items
    noteIds.forEach(noteId => {
        const listItem = document.createElement('li');
        listItem.textContent = noteId.toString();
        listElement.appendChild(listItem);
    });
}
