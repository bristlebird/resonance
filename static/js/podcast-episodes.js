const editButtons = document.getElementsByClassName("btn-edit");
const episodeTitle = document.getElementById("id_title");
const episodeText = document.getElementById("id_description");
const episodeForm = document.getElementById("episodeForm");
const submitButton = document.getElementById("submitButton");

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
    let episodeId = e.target.getAttribute("data-episode_id");
    let episodeTitleVal = document.getElementById(`episodeTitle${episodeId}`).innerText;
    let episodeDescVal = document.getElementById(`episodeDesc${episodeId}`).innerText;
    episodeTitle.value = episodeTitleVal;
    episodeText.value = episodeDescVal;
    submitButton.innerText = "Update";
    episodeForm.setAttribute("action", `edit_episode/${episodeId}`);
  });
}