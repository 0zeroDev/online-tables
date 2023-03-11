function updateCell(cell) {
  var updated_cell = {
    cell_x: cell.getAttribute("x"),
    cell_y: cell.getAttribute("y"),
    cell_content: cell.textContent,
  };

  $.ajax({
    url: "/update_cell",
    type: "POST",
    data: updated_cell,
    success: function (response) {
      console.log(response);
    },
    error: function (xhr) {
      console.log(xhr.responseText);
    },
  });
}
