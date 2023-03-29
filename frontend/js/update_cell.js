$("td").on("focus", function () {
  // Save the original content of the cell as a data attribute
  $(this).data("original-content", $(this).text());

  // Display the formula in the cell
  $(this).text($(this).data("formula"));
});

$("td").on("blur", function () {
  var cell = this;

  // Update the formula in the data attribute
  $(this).data("formula", $(this).text());

  // Pass a function as the second argument to the updateCell function
  updateCell(cell, function (calculated_cell) {
    $(cell).text(calculated_cell);
  });
});

function updateCell(cell, callback) {
  var updated_cell = {
    cell_x: cell.getAttribute("x"),
    cell_y: cell.getAttribute("y"),
    cell_content: cell.textContent,
  };

  $.ajax({
    url: "/update_cell",
    type: "POST",
    data: updated_cell,
    success: function (calculated_cell) {
      // Check if the callback argument is a function
      if (typeof callback === "function") {
        callback(calculated_cell);
      }
    },
    error: function (xhr) {
      console.log(xhr.responseText);
    },
  });
}
