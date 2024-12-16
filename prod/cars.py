CARS = {
    'vw':{
        "cc": "https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&verified.VIN=1&categories.main.id=1&brand.id[0]=84&model.id[0]=3006&country.import.usa.not=-1&price.currency=1&sort[0].order=dates.created.desc&abroad.not=0&custom.not=1&size=10&page=",
        "golf": "https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&verified.VIN=1&categories.main.id=1&brand.id[0]=84&model.id[0]=35449&country.import.usa.not=-1&price.currency=1&sort[0].order=dates.created.desc&abroad.not=0&custom.not=1&size=10&page=",
        "jetta": "https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&verified.VIN=1&categories.main.id=1&brand.id[0]=84&model.id[0]=785&country.import.usa.not=-1&price.currency=1&sort[0].order=dates.created.desc&abroad.not=0&custom.not=1&size=10&page=",
        "passat": "https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&verified.VIN=1&categories.main.id=1&brand.id[0]=84&model.id[0]=39690&country.import.usa.not=-1&price.currency=1&sort[0].order=dates.created.desc&abroad.not=0&custom.not=1&size=10&page=",
        "polo": "https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&verified.VIN=1&categories.main.id=1&brand.id[0]=84&model.id[0]=789&country.import.usa.not=-1&price.currency=1&sort[0].order=dates.created.desc&abroad.not=0&custom.not=1&size=10&page=",
        "tiguan": "https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&verified.VIN=1&categories.main.id=1&brand.id[0]=84&model.id[0]=2692&country.import.usa.not=-1&price.currency=1&sort[0].order=dates.created.desc&abroad.not=0&custom.not=1&size=10&page=",
        "touareg": "https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&verified.VIN=1&categories.main.id=1&brand.id[0]=84&model.id[0]=793&country.import.usa.not=-1&price.currency=1&sort[0].order=dates.created.desc&abroad.not=0&custom.not=1&size=10&page=",
        "touran": "https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&verified.VIN=1&categories.main.id=1&brand.id[0]=84&model.id[0]=2093&country.import.usa.not=-1&price.currency=1&sort[0].order=dates.created.desc&abroad.not=0&custom.not=1&size=10&page=",
        "egolf": "https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&verified.VIN=1&categories.main.id=1&brand.id[0]=84&model.id[0]=45152&country.import.usa.not=-1&price.currency=1&sort[0].order=dates.created.desc&abroad.not=0&custom.not=1&size=10&page=",
    },
    'bmw': {
        "series1": "https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&verified.VIN=1&categories.main.id=1&brand.id[0]=9&model.id[0]=2161&country.import.usa.not=-1&price.currency=1&sort[0].order=dates.created.desc&abroad.not=0&custom.not=1&size=10&page=",
        "series3": "https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&verified.VIN=1&categories.main.id=1&brand.id[0]=9&model.id[0]=3219&country.import.usa.not=-1&price.currency=1&sort[0].order=dates.created.desc&abroad.not=0&custom.not=1&size=10&page=",
        "series4": "https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&verified.VIN=1&categories.main.id=1&brand.id[0]=9&model.id[0]=42495&country.import.usa.not=-1&price.currency=1&sort[0].order=dates.created.desc&abroad.not=0&custom.not=1&size=10&page=",
        "series5": "https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&verified.VIN=1&categories.main.id=1&brand.id[0]=9&model.id[0]=2319&country.import.usa.not=-1&price.currency=1&sort[0].order=dates.created.desc&abroad.not=0&custom.not=1&size=10&page=",
        "series7": "https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&verified.VIN=1&categories.main.id=1&brand.id[0]=9&model.id[0]=18490&country.import.usa.not=-1&price.currency=1&sort[0].order=dates.created.desc&abroad.not=0&custom.not=1&size=10&page=",
        "x1": "https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&verified.VIN=1&categories.main.id=1&brand.id[0]=9&model.id[0]=3597&country.import.usa.not=-1&price.currency=1&sort[0].order=dates.created.desc&abroad.not=0&custom.not=1&size=10&page=",
        "x3": "https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&verified.VIN=1&categories.main.id=1&brand.id[0]=9&model.id[0]=1866&country.import.usa.not=-1&price.currency=1&sort[0].order=dates.created.desc&abroad.not=0&custom.not=1&size=10&page=",
        "x5": "https://auto.ria.com/uk/search/?indexName=auto,order_auto,newauto_search&verified.VIN=1&categories.main.id=1&brand.id[0]=9&model.id[0]=96&country.import.usa.not=-1&price.currency=1&sort[0].order=dates.created.desc&abroad.not=0&custom.not=1&size=10&page=",
    },
}


def get_models():
    models = ["all"]
    for brand, models_dict in CARS.items():
        for model in models_dict.keys():
            models.append(model)
    return models