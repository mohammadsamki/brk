$(document).ready(function() {

    // Add to cart function
    function addToCart(price, item, query, country, issuer, item_index) {
        $.ajax({
            url: '/add_to_cart/',
            type: 'POST',
            data: {
                'price': price,
                'item': item,
                'query': query,
                'country': country,
                'issuer': issuer,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                if (response.success) {
                    // Update the button to show the item has been added
                    $('#button_cart_' + item_index).removeClass('btn').addClass('btn-success').prop('disabled', true).text('Added to cart');

                    // Update the cart item count
                    cartItemCount = cartItemCount+1;
                    $('#count_cart_items').text(cartItemCount);
                    
                } else {
                    alert('Error adding item to cart');
                }
            }
        });
    }

    // Bind the click event to the "Add to cart" buttons
    $('.add-to-cart-btn').on('click', function() {
        var price = $(this).data('price');
        var item = $(this).data('item');
        var query = $(this).data('query');
        var country = $(this).data('country');
        var issuer = $(this).data('issuer');
        var item_index = $(this).data('index');

        addToCart(price, item, query, country, issuer, item_index);
    });

    // Remove selected items function
    function removeSelectedItems() {
        // Get the selected cart item IDs
        var selected_item_ids = [];
        $('.cart-item-checkbox:checked').each(function() {
            selected_item_ids.push($(this).data('item-id'));
        });

        if (selected_item_ids.length === 0) {
            alert('Please select at least one item to remove');
            return;
        }

        // Display a SweetAlert2 confirmation message
        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'
        }).then((result) => {
            if (result.isConfirmed) {
                // Proceed with the removal if the user confirms
                $.ajax({
                    url: '/remove_selected_from_cart/',
                    type: 'POST',
                    data: {
                        'item_ids': JSON.stringify(selected_item_ids),
                        'csrfmiddlewaretoken': csrfToken
                    },
                    success: function(response) {
                        if (response.success) {
                            // Remove the selected cart items from the table
                            $('.cart-item-checkbox:checked').each(function() {
                                $(this).closest('tr').remove();
                            });

                            // Update the cart item count
                            cartItemCount = cartItemCount - selected_item_ids.length;
                            $('#count_cart_items').text(cartItemCount);

                            // Show a success message
                            Swal.fire(
                                'Deleted!',
                                'The selected items have been removed from the cart.',
                                'success'
                            );
                        } else {
                            Swal.fire(
                                'Error',
                                'Error removing selected items from cart.',
                                'error'
                            );
                        }
                    }
                });
            }
        });
    }

    // Bind the click event to the "Remove Selected" button
    $('#remove-selected-btn').on('click', function() {
        removeSelectedItems();
    });

    function errorPayment() {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'You dont have Balance!',
            footer: '<a href="/Billing">to top up your balance</a>'
        })
    }
});