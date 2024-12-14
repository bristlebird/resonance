// ====================================================================
// SCRIPTS FOR EDITING PODCAST EPISODES
// ====================================================================
// Adds click handlers to delete buttons & confirmation modals

/**
* Initializes deletion functionality for the podcast delete buttons.
* 
* For each button in the `deletePcBtns` collection:
* - Retrieves the associated podcast's ID upon click.
* - Updates the `deletePcConfirm` link's href to point to the 
* deletion endpoint for the specific episode.
* - Displays a confirmation modal (`deletePcModal`) to prompt 
* the user for confirmation before deletion.
*/
const deletePcBtns = document.getElementsByClassName("btn-delete-podcast");
const deletePcModal = new bootstrap.Modal(document.getElementById("deletePcModal"));
const deletePcConfirm = document.getElementById("deletePcConfirm");
for (let button of deletePcBtns) {
    button.addEventListener("click", (e) => {
      let pcId = e.target.getAttribute("data-podcast_id");
      deletePcConfirm.href = `delete-podcast/${pcId}`;
      deletePcModal.show();
    });
}

/**
* Initializes deletion functionality for the episode delete buttons.
* 
* For each button in the `deleteEpBtns` collection:
* - Retrieves the associated episode's ID upon click.
* - Updates the `deleteEpConfirm` link's href to point to the 
* deletion endpoint for the specific episode.
* - Displays a confirmation modal (`deleteEpModal`) to prompt 
* the user for confirmation before deletion.
*/
const deleteEpBtns = document.getElementsByClassName("btn-delete-episode");
const deleteEpModal = new bootstrap.Modal(document.getElementById("deleteEpModal"));
const deleteEpConfirm = document.getElementById("deleteEpConfirm");
for (let button of deleteEpBtns) {
    button.addEventListener("click", (e) => {
      let epId = e.target.getAttribute("data-episode_id");
      deleteEpConfirm.href = `delete-episode/${epId}`;
      deleteEpModal.show();
    });
}
