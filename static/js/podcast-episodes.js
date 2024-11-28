const editButtons = document.getElementsByClassName("btn-edit");
const epTitle = document.getElementById("id_title");
const epText = document.getElementById("id_description");
const epAuthor = document.getElementById("id_author");
const epKeywords = document.getElementById("id_keywords");
const epType = document.getElementById("id_type");
const epSeasonNum = document.getElementById("id_season_number");
const epEpNum = document.getElementById("id_episode_number");
const epExplicit = document.getElementById("id_explicit_content_warning");
const epAltEpUrl = document.getElementById("id_alt_episode_url");
const epVideoUrl = document.getElementById("id_video_url");
const epStatus = document.getElementById("id_status");
const epForm = document.getElementById("episodeForm");
const submitButton = document.getElementById("submitButton");

const deleteModal = new bootstrap.Modal(document.getElementById("deleteModal"));
const deleteButtons = document.getElementsByClassName("btn-delete");
const deleteConfirm = document.getElementById("deleteConfirm");

/**
* Initializes edit functionality for the provided edit buttons.
* 
* For each button in the `editButtons` collection:
* - Retrieves the associated episode's ID upon click.
* - Fetches the content of the corresponding episode.
* - Populates the `episodeText` input/textarea with the episode's content for editing.
* - Updates the submit button's text to "Update".
* - Sets the form's action attribute to the `edit_episode/{episodeId}` endpoint.
*/
for (let button of editButtons) {
  button.addEventListener("click", (e) => {
    let epId = e.target.getAttribute("data-episode_id");
    // let epTitleVal = document.getElementById(`epTitle${epId}`).innerText;
    // let epDescVal = document.getElementById(`epDesc${epId}`).innerText;
    // let epAuthorVal = document.getElementById(`epAuthor${epId}`).innerText;
    // let epKeywordsVal = document.getElementById(`epKeywords${epId}`).innerText;
    // let epTypeVal = document.getElementById(`epType${epId}`).innerText;
    // let epSeasonNumVal = document.getElementById(`epAuthor${epId}`).innerText;
    // let epAuthorVal = document.getElementById(`epAuthor${epId}`).innerText;
    // let epAuthorVal = document.getElementById(`epAuthor${epId}`).innerText;
    // let epAuthorVal = document.getElementById(`epAuthor${epId}`).innerText;
    // let epAuthorVal = document.getElementById(`epAuthor${epId}`).innerText;
    // let epAuthorVal = document.getElementById(`epAuthor${epId}`).innerText;
    // epTitle.value = epTitleVal;
    // epText.value = epDescVal;
    // epAuthor.value = epAuthorVal;
    epTitle.value = document.getElementById(`epTitle${epId}`).innerText;
    epText.value = document.getElementById(`epDesc${epId}`).innerText;
    epAuthor.value = document.getElementById(`epAuthor${epId}`).innerText;
    epKeywords.value = document.getElementById(`epKeywords${epId}`).innerText;
    epType.value = document.getElementById(`epType${epId}`).innerText;
    epSeasonNum.value = document.getElementById(`epSeasonNum${epId}`).innerText;
    epEpNum.value = document.getElementById(`epEpNum${epId}`).innerText;
    epExplicit.value = document.getElementById(`epExplicit${epId}`).innerText;
    epAltEpUrl.value = document.getElementById(`epAltEpUrl${epId}`).innerText;
    epVideoUrl.value = document.getElementById(`epVideoUrl${epId}`).innerText;
    epStatus.value = document.getElementById(`epStatus${epId}`).innerText;
    submitButton.innerText = "Update";
    epForm.setAttribute("action", `edit_episode/${epId}`);
  });
}

/**
* Initializes deletion functionality for the provided delete buttons.
* 
* For each button in the `deleteButtons` collection:
* - Retrieves the associated episode's ID upon click.
* - Updates the `deleteConfirm` link's href to point to the 
* deletion endpoint for the specific episode.
* - Displays a confirmation modal (`deleteModal`) to prompt 
* the user for confirmation before deletion.
*/
for (let button of deleteButtons) {
    button.addEventListener("click", (e) => {
      let epId = e.target.getAttribute("data-episode_id");
      deleteConfirm.href = `delete_episode/${epId}`;
      deleteModal.show();
    });
}