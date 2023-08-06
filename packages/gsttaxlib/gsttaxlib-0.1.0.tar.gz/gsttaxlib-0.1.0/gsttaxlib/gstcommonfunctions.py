
def fetch_company_rec(file, file_ref, http_response, FileWrapper):
    response = http_response(FileWrapper(file), content_type="application/zip")
    response['Content-Length'] = file.size
    response['Content-Disposition'] = 'attachment; filename=' + file_ref
    response.write(file.read())
    return response


def calculate_rating(existingRating, currUserRating, numOfVotes):
    new_rating = (existingRating + float(currUserRating)) / numOfVotes
    return new_rating
