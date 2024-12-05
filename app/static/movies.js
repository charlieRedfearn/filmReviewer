$(document).ready(function(){
    // AJAX: Filter and Sort Films
    $('#filter_btn').on('click', function () {
        const genre = $('#genre').val();
        const sort_by = $('#sort_by').val();

        $.ajax({
            url: '/api/films',
            data: { genre, sort_by },
            success: function (films) {
                let html = '';
                films.forEach(film => {
                    html += `
                        <div class="movieContainer">
                            <div class="movie">
                                <h3>${film.title} (${film.release_year})</h3>
                                <h4>${film.description}</h4>
                            </div>
                            <div class="submitReview">
                                <h3>Submit a Review:</h3>
                                <textarea id="review_content-${film.id}" class="form-control"></textarea>
                                <label for="rating-${film.id}">Rating:</label>
                                <select id="rating-${film.id}">
                                    <option value="1">1</option>
                                    <option value="2">2</option>
                                    <option value="3">3</option>
                                    <option value="4">4</option>
                                    <option value="5">5</option>
                                </select>
                                <button  class="btn btn-secondary btn-sm" onclick="submit_review(${film.id}, $('#review_content-${film.id}').val(),$('#rating-${film.id}').val())">Submit Review</button>
                            </div>
                            <div class="reviewText"><h4>Reviews</h4></div>
                    `;
                    film.reviews.forEach(review => {
                        html += `
                            <div class="review">
                                <h4>${review.username} (${review.rating}/5)</h4>
                                <p>${review.content}</p>
                                <button onclick="likeReview(${review.id})">Like</button>
                                <span id="likes-count-${review.id}">${review.likes_count}</span>
                                <button onclick="unLikeReview(${review.id})">Unlike</button>
                            </div>
                        `;
                    });
                    html +=`</div>`
                });
                $('#movies_list').html(html);
            }
        });
    });

});

function submit_review(film_id, content, rating) {
    $.ajax({
        url: '/api/reviews',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ film_id, content, rating }),
        // adds new review to review list
        success: function (review) {
            $('#filter_btn').click();
        }
    });
};

function likeReview(review_id) {
    $.ajax({
        url: `/api/reviews/${review_id}/like`,
        method: 'POST',
        success: function (data) {
            if(data.liked){
                $(`#likes-count-${review_id}`).text(data.likes_count);
            }
            else{
                alert("You have already liked this review");
            }
        }
    });
}

function unLikeReview(review_id) {
    $.ajax({
        url: `/api/reviews/${review_id}/unLike`,
        method: 'POST',
        success: function (data) {
            if(data.unLiked){
                $(`#likes-count-${review_id}`).text(data.likes_count);
            }
            else{
                alert("Cannot unlike - has not been liked");
            }
        }
    });
}