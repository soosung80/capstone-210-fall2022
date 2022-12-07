import ListLi from './ListLi';
import { Text } from '@aws-amplify/ui-react';

export default function ItemList({ items, handleCheck, handleDelete }) {

  return (
    <>
      {
        items.length ? (
          <ListLi
            items={items}
            handleCheck={handleCheck}
            handleDelete={handleDelete}
          />
        ) : (
          <Text align="center" as="p" style={{ marginTop: "1.5rem" }}>Empty list.</Text>
        )
      }
    </>
  )
}