def input_image_setup(rule_image_name, density_image_name):
    '''
    Loads the rule-image and population-density-image from the filesystem.
    Saves the density image in /temp/ folder so that it could be ensured.

    Parameters
    ----------
    rule_image_name: String
        Name of the rule_image specified in Parameters
    density_image_name: String
        Name of the density_image specified in Parameters

    Returns
    --------
    rule_img: np.ndarray
        Rule-image as numpy array
    density_img: np.ndarray
        Density-image as numpy array
    '''
    # Load the rule image
    rule_img = cv2.imread(rule_image_name, cv2.IMREAD_GRAYSCALE)
    # Load the density image
    density_img = cv2.imread(density_image_name, cv2.IMREAD_GRAYSCALE)
    # Save the density image in temp folder
    cv2.imwrite('temp/density_image.png', density_img)
    return rule_img, density_img