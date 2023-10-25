$(document).ready(function() {

    // Hide the addCupcake Form
    $('#cupcake-form').hide();

    // Show or hide form when button is clicked
    $('#show-form-button').click(function(event) {
        event.preventDefault();
        $('#cupcake-form').toggle();
    });

    // Initial load of cupcake
    loadCupcakes();

     // Form submission
     $('#cupcake-form').submit(function(event) {
        event.preventDefault();

        // Get form data
        const flavor = $('#flavor').val();
        const size = $('#size').val();
        const rating = $('#rating').val();
        const image = $('#image').val();

        //Create cupcake obj
        const newCupcake = {
            flavor: flavor,
            size: size,
            rating: rating,
            image: image
        };

        //Send a POST request to create new cupcake
        axios.post('/api/cupcakes', newCupcake)
            .then(function(response) {
                //Clear form fields
                $('#flavor').val('');
                $('#size').val('');
                $('#rating').val('');
                $('#image').val('');
                alert('Cupcake added successfully')

                //Hide form again
                $('#cupcake-form').hide();

                loadCupcakes();
            })
            .catch(function(error) {
                console.error('Error creating cupcake', error)
            });
        });

        //Handle delete button
       
        $('#cupcakes-list').on('click', '.delete-button', function() {
            const id = $(this).data('id');
            console.log('Clicked btn with the id:', id)
            const cardToRemove = $(this).closest('.card');

            // Send a DELETE request
            axios.delete(`/api/cupcakes/${id}`)
                .then(function(response) {
                    cardToRemove.remove();
                })
                .catch(function(error) {
                    console.error('Error deleting cupcake', error)
                });
        });

        function loadCupcakes() {
            axios.get('/api/cupcakes')
            .then(function(response) {
                const cupcakes = response.data.cupcakes;
                const cupcakesList = $('#cupcakes-list');
    
                // Clear current list
                cupcakesList.empty();
    
                //Add each cupcake to the list
                cupcakes.forEach(function(cupcake) {
                    cupcakesList.append
                    (`
                    <div class="col-4 mb-4">
                        <div class="card">
                            <img src="${cupcake.image}" 
                                 class="card-img-top" 
                                 alt="default_pic" 
                                 style="max-width: 200px; max-height: 250px;">
                            <div class="card-body">
                                <h5 class="card-title">${cupcake.flavor}</h5>
                                <p class="card-text">Rating: ${cupcake.rating}</p>
                                <p class="card-text">Size: ${cupcake.size}</p>
                                <button class="btn btn-danger delete-button" 
                                        data-id="${cupcake.id}">X
                                </button>
                            </div>
                        </div>
                    </div>
                    `);
                });
            })
            .catch(function(error) {
                console.error('Error loading cupcakes:', error );
            });
        }
        $('#save-cupcake-button').click(function() {
            $('#cupcake-form').show();
        });
    });
