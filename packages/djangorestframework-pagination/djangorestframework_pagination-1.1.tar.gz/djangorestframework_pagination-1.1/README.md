example:

```
class TestAPI(APIView):

    @staticmethod
    def get(request):
        tests = Test.objects.all() # filter or order by or anything else
        
        pagination = PaginationObject(objects=tests, page=1, numbers_in_page=10, 
                     serializer=TestSerializer)

        return Response(pagination.serializer_data(), status=status.HTTP_200_OK)
```

to get all objects in one page :

```
        pagination = PaginationObject(objects=tests, page=1, numbers_in_page=-1, 
                     serializer=TestSerializer)
```